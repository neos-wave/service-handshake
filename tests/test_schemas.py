# Copyright 2026 Neos Wave Ltd. Licensed under the Apache License, Version 2.0.
"""Structural tests only. No credential authenticity or runtime enforcement is tested."""
import copy, hashlib, json, unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text())
D=read('sh-1.2.schema.json'); A=read('sh-1.2.action-assessment.schema.json'); OLD=read('sh-1.1.schema.json')
def valid(schema,value): return Draft202012Validator(schema,format_checker=FormatChecker()).is_valid(value)
class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.c=read('examples/assisted-consumer.json'); self.a=read('examples/refund-held.json')
    def test_schemas_are_well_formed(self):
        for s in [D,A,OLD]: Draft202012Validator.check_schema(s)
    def test_all_examples(self):
        for f in (ROOT/'examples').glob('*.json'):
            with self.subTest(file=f.name): self.assertTrue(valid(A if 'assessment_id' in json.loads(f.read_text()) else D,json.loads(f.read_text())))
    def test_old_minimum_remains_valid_under_old_schema(self):
        v={'protocol_version':'SH-1.1','principal_id':'p','agent_id':'a','goals':{'primary_goal':'Help','non_goals':['No changes']}}
        self.assertTrue(valid(OLD,v)); self.assertFalse(valid(D,v))
    def test_new_version_is_not_valid_under_old_schema(self): self.assertFalse(valid(OLD,self.c))
    def test_assisted_needs_disclosure(self):
        del self.c['disclosure']; self.assertFalse(valid(D,self.c))
    def test_assisted_needs_confirmation_record(self):
        del self.c['confirmation']; self.assertFalse(valid(D,self.c))
    def test_confirmation_needs_actor_time_method(self):
        del self.c['confirmation']['confirmer_ref']; self.assertFalse(valid(D,self.c))
    def test_confirmation_is_not_authority(self):
        self.assertTrue(valid(D,self.c)); self.assertNotIn('delegation_proof',self.c['authority_level']); self.assertEqual(self.a['decision'],'hold')
    def test_unknown_confirmed_status_rejected(self):
        self.c['confirmation']['status']='verified'; self.assertFalse(valid(D,self.c))
    def test_injected_verifier_field_rejected(self):
        self.c['verified']=True; self.assertFalse(valid(D,self.c))
    def test_invalid_timestamp_rejected(self):
        self.c['confirmation']['confirmed_at']='yesterday'; self.assertFalse(valid(D,self.c))
    def test_empty_claim_arrays_are_structural_not_grants(self):
        self.c['authority_level']['authority_scope']=[]; self.c['goals']['non_goals']=[];self.assertTrue(valid(D,self.c))
    def test_precedence_field_supported(self):
        self.c['fallback_rules']['precedence_logic']='CONSUMER_PRIORITY';self.assertTrue(valid(D,self.c))
    def test_safeguarding_trigger_required_in_fallback_object(self):
        self.c['fallback_rules']['fallback_triggers']=[{'if_unresolved_after_loops':3}];self.assertFalse(valid(D,self.c))
    def test_retention_example_uses_supported_value(self):
        self.c['data_permissions']['retention_policy']={'policy':'retain_per_legal_requirement'};self.assertTrue(valid(D,self.c));self.c['data_permissions']['retention_policy']['policy']='mandatory_audit_retention';self.assertFalse(valid(D,self.c))
    def test_financial_limit_aggregate_requires_period(self):
        b=read('examples/brand.json');b['authority_level']['financial_limits'][0]['basis']='aggregate_period';self.assertFalse(valid(D,b));b['authority_level']['financial_limits'][0]['period_seconds']=86400;self.assertTrue(valid(D,b))
    def test_currency_and_minor_units(self):
        self.a['action']['financial']['amount_minor']=4.5;self.assertFalse(valid(A,self.a));self.a['action']['financial']['amount_minor']=4000;self.a['action']['financial']['currency']='pounds';self.assertFalse(valid(A,self.a))
    def test_non_allow_requires_reason_and_no_execution(self):
        self.a['reasons']=[];self.assertFalse(valid(A,self.a));self.a=read('examples/refund-held.json');self.a['execution']={'status':'completed','receipt_ref':'r'};self.assertFalse(valid(A,self.a))
    def test_live_safeguarding_cannot_structurally_allow(self):
        self.a['action']['category']='public_information';self.a['decision']='allow';self.a['action']['safeguarding_required']=True;self.assertFalse(valid(A,self.a))
    def test_protected_allow_needs_verification_record(self):
        self.a['decision']='allow';self.assertFalse(valid(A,self.a))
    def test_public_information_can_have_no_delegation(self):
        self.a['decision']='allow';self.a['action']['category']='public_information';self.a['action']['action_type']='explain_public_policy';self.a['action'].pop('financial');self.a['reasons']=[];self.assertTrue(valid(A,self.a))
    def test_verified_allow_requires_expiry_and_replay(self):
        v=self.synthetic_allow();self.assertTrue(valid(A,v));del v['replay_control_ref'];self.assertFalse(valid(A,v))
    def test_verified_allow_requires_both_parties(self):
        v=self.synthetic_allow();v['verification_results']=v['verification_results'][:1];self.assertFalse(valid(A,v))
    def test_revoked_evidence_cannot_structurally_allow(self):
        v=self.synthetic_allow();v['verification_results'][0]['result']='revoked';self.assertFalse(valid(A,v))
    def test_failed_binding_cannot_structurally_allow(self):
        v=self.synthetic_allow();v['verification_results'][0]['binding_verified']=False;self.assertFalse(valid(A,v))
    def test_completed_requires_receipt(self):
        v=self.synthetic_allow();v['execution']['status']='completed';self.assertFalse(valid(A,v));v['execution']['receipt_ref']='synthetic-receipt';self.assertTrue(valid(A,v))
    def test_both_declaration_roles_required(self):
        self.a['declarations'][1]['party_role']='consumer';self.assertFalse(valid(A,self.a))
    def test_stored_declaration_digests_match_exact_example_bytes(self):
        for f,role in [('assisted-consumer.json','consumer'),('brand.json','company')]:
            digest=hashlib.sha256((ROOT/'examples'/f).read_bytes()).hexdigest()
            self.assertEqual(next(d['sha256'] for d in self.a['declarations'] if d['party_role']==role),digest)
    def test_unbounded_recurrence_rejected(self):
        self.a['action']['financial']['recurrence']={'interval_seconds':2592000};self.assertFalse(valid(A,self.a))
    @staticmethod
    def synthetic_allow():
        # Deliberately synthetic structural fixture. A real verifier must authenticate and bind these fields.
        v=read('examples/refund-held.json');v.update(profile='verified_authority',decision='allow',reasons=[],expires_at='2026-09-28T09:05:00Z',replay_control_ref='synthetic-one-use-reservation')
        v['verification_results']=[{'party_role':role,'evidence_ref':'synthetic-'+role,'mechanism':'synthetic-test-only','issuer_ref':'synthetic-issuer','subject_ref':role,'requester_ref':'synthetic-session','audience_ref':'synthetic-service','proposal_id':v['action']['proposal_id'],'scope':['refund'],'verified_by':'synthetic-verifier','verified_at':'2026-09-28T09:02:00Z','valid_from':'2026-09-28T09:00:00Z','valid_to':'2026-09-28T09:05:00Z','status_checked_at':'2026-09-28T09:02:00Z','status_method':'synthetic-status','result':'verified','binding_verified':True} for role in ['consumer','company']]
        return v
if __name__=='__main__': unittest.main(verbosity=2)
