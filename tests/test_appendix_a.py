# Copyright 2026 Neos Wave Ltd. Licensed under the Apache License, Version 2.0.
"""Appendix A representation checks, not evidence or execution tests.

Fixtures are copies for schema validation only. They are not approved proposals;
changing an actual proposal requires a new ID and fresh assessment/bindings.
"""
import copy
import unittest
from test_schemas import A, D, read, valid

CORE = {
    'refund': ['request_refund', 'offer_refund', 'accept_refund', 'issue_refund'],
    'replacement': ['request_replacement', 'offer_replacement', 'accept_replacement', 'arrange_replacement'],
    'repair': ['request_repair', 'offer_repair', 'accept_repair', 'arrange_repair'],
    'voucher': ['request_voucher', 'offer_voucher', 'accept_voucher', 'issue_voucher'],
    'cancellation': ['request_cancellation', 'offer_cancellation', 'accept_cancellation', 'execute_cancellation'],
    'appointment': ['request_appointment', 'offer_appointment', 'accept_appointment', 'book_appointment'],
}

class AppendixARepresentationTests(unittest.TestCase):
    def test_all_core_outcomes_and_role_identifiers_fit(self):
        for outcome, roles in CORE.items():
            with self.subTest(outcome=outcome):
                assessment=read('examples/refund-held.json')
                assessment['action']['action_type']=outcome
                self.assertTrue(valid(A, assessment))
                declaration=read('examples/brand.json')
                declaration['options_constraints']['allowed_actions']=roles
                declaration['authority_level']['authority_scope']=roles
                declaration['authority_level']['financial_limits'][0]['action_type']=outcome
                self.assertTrue(valid(D, declaration))

    def test_namespaced_extensions_fit_relevant_action_fields(self):
        name='acme:retention_offer'
        declaration=read('examples/brand.json')
        declaration['options_constraints']['allowed_actions']=[name]
        declaration['authority_level']['authority_scope']=[name]
        declaration['authority_level']['financial_limits'][0]['action_type']=name
        self.assertTrue(valid(D, declaration))
        assessment=read('examples/refund-held.json')
        assessment['action']['action_type']=name
        self.assertTrue(valid(A, assessment))

    def test_cancellation_and_appointment_terms_can_be_represented(self):
        terms={
            'cancellation': {
                'service_ref':'synthetic-service', 'scope':'full',
                'effective_at':'2026-10-01T09:00:00+01:00', 'time_zone':'Europe/London',
                'charges_minor':0, 'refund_minor':0, 'remaining_obligations':'none',
                'return_duties':'none', 'continuing_services_effect':'none',
                'access_effect':'ends at effective_at',
            },
            'appointment': {
                'service':'synthetic appointment', 'provider_ref':'synthetic-provider',
                'participant_ref':'synthetic-participant',
                'starts_at':'2026-10-01T09:00:00+01:00', 'time_zone':'Europe/London',
                'duration_minutes':30, 'delivery_channel':'telephone',
                'deposit_minor':0, 'payment_timing':'no payment due',
                'cancellation_terms':'no fee', 'rescheduling_terms':'no fee',
                'no_show_terms':'no fee', 'access_needs':'none stated',
                'confirmation_conditions':'none',
            },
        }
        for action, material_terms in terms.items():
            with self.subTest(action=action):
                fixture=read('examples/refund-held.json')
                fixture['action']['action_type']=action
                fixture['action']['material_terms']=material_terms
                fixture['action']['financial']={'amount_minor':0,'currency':'GBP','currency_exponent':2}
                self.assertTrue(valid(A, fixture))

    def test_complex_terms_need_flat_values_or_an_immutable_reference(self):
        fixture=read('examples/refund-held.json')
        for unsupported in [{'nested':{'value':'x'}}, {'list':['x']}]:
            with self.subTest(unsupported=unsupported):
                fixture['action']['material_terms']=unsupported
                self.assertFalse(valid(A,fixture))
        fixture['action']['material_terms']={'terms_record_ref':'synthetic-immutable-record-v1'}
        self.assertTrue(valid(A,fixture))

    def test_structure_alone_does_not_establish_complete_material_terms(self):
        # Deliberately incomplete: an application must hold, despite schema acceptance.
        for outcome in ['cancellation','appointment']:
            fixture=read('examples/refund-held.json')
            fixture['action']['action_type']=outcome
            for incomplete in [{}, {'effective_at':None}]:
                with self.subTest(outcome=outcome, terms=incomplete):
                    fixture['action']['material_terms']=incomplete
                    self.assertTrue(valid(A,fixture))
                    self.assertEqual(fixture['decision'],'hold')

if __name__=='__main__': unittest.main()
