import unittest
from flow import RuleIntermediator as RI


class TestFlow(unittest.TestCase):

    ############################################################
    #################### Rule Intermediator ####################
    ############################################################

    def test_fetchRules_when_oneRuleExists(self):
        # Arrange
        object_name = "Host_10.0.0.1"

        filtered_list = [
            {
                "rule": {"uid": "4"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Standard"},
            }
        ]

        expected_uids_policy_standard = ["4"]

        expected_policy_standard = "Standard"

        # Act
        result = RI.fetch_rules(object_name, filtered_list)

        result_uids_standard = result[0].access_rules_uid

        result_policy_standard = result[0].policy

        # Assert
        self.assertEqual(result_uids_standard, expected_uids_policy_standard)

        self.assertEqual(result_policy_standard, expected_policy_standard)

    def test_fetchRules_when_oneRuleEachPolicyExists(self):
        # Arrange
        object_name = "Host_10.0.0.1"

        filtered_list = [
            {
                "rule": {"uid": "4"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Standard"},
            },
            {
                "rule": {"uid": "2"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Premium"},
            },
        ]

        expected_uids_policy_standard = ["4"]
        expected_uids_policy_premium = ["2"]

        expected_policy_standard = "Standard"
        expected_policy_premium = "Premium"

        # Act
        result = RI.fetch_rules(object_name, filtered_list)

        result_uids_standard = result[0].access_rules_uid
        result_uids_premium = result[1].access_rules_uid

        result_policy_standard = result[0].policy
        result_policy_premium = result[1].policy

        # Assert
        self.assertEqual(result_uids_standard, expected_uids_policy_standard)
        self.assertEqual(result_uids_premium, expected_uids_policy_premium)

        self.assertEqual(result_policy_standard, expected_policy_standard)
        self.assertEqual(result_policy_premium, expected_policy_premium)

    def test_fetchRules_when_multipleRulesExists(self):
        # Arrange
        object_name = "Host_10.0.0.1"

        filtered_list = [
            {
                "rule": {"uid": "4"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Standard"},
            },
            {
                "rule": {"uid": "10"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Standard"},
            },
            {
                "rule": {"uid": "2"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Premium"},
            },
            {
                "rule": {"uid": "5"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Premium"},
            },
            {
                "rule": {"uid": "78"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Premium"},
            },
        ]

        expected_uids_policy_standard = ["4", "10"]
        expected_uids_policy_premium = ["2", "5", "78"]

        expected_policy_standard = "Standard"
        expected_policy_premium = "Premium"

        # Act
        result = RI.fetch_rules(object_name, filtered_list)

        result_uids_standard = result[0].access_rules_uid
        result_uids_premium = result[1].access_rules_uid

        result_policy_standard = result[0].policy
        result_policy_premium = result[1].policy

        # Assert
        self.assertEqual(result_uids_standard, expected_uids_policy_standard)
        self.assertEqual(result_uids_premium, expected_uids_policy_premium)

        self.assertEqual(result_policy_standard, expected_policy_standard)
        self.assertEqual(result_policy_premium, expected_policy_premium)

    #################### filter_layer_type() ####################
    def test_filterLayerType_when_noneExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "2"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "3"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "4"}, "layer": {"type": "threat-layer"}},
        ]

        expected_result = []

        # Act
        result = RI.filter_layer_type(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    def test_filterLayerType_when_oneExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "layer": {"type": "access-layer"}},
            {"rule": {"uid": "2"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "3"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "4"}, "layer": {"type": "threat-layer"}},
        ]

        expected_result = [{"rule": {"uid": "1"}, "layer": {"type": "access-layer"}}]

        # Act
        result = RI.filter_layer_type(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    def test_filterLayerType_when_multipleExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "layer": {"type": "access-layer"}},
            {"rule": {"uid": "2"}, "layer": {"type": "access-layer"}},
            {"rule": {"uid": "3"}, "layer": {"type": "threat-layer"}},
            {"rule": {"uid": "4"}, "layer": {"type": "access-layer"}},
        ]

        expected_result = [
            {"rule": {"uid": "1"}, "layer": {"type": "access-layer"}},
            {"rule": {"uid": "2"}, "layer": {"type": "access-layer"}},
            {"rule": {"uid": "4"}, "layer": {"type": "access-layer"}},
        ]

        # Act
        result = RI.filter_layer_type(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    #################### order_by_package_name() ####################
    def test_orderByPackageName_when_multipleExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
            {"rule": {"uid": "2"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "3"}, "package": {"name": "Standard"}},
            {"rule": {"uid": "4"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "5"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "6"}, "package": {"name": "Isonet"}},
            {"rule": {"uid": "7"}, "package": {"name": "Premium"}},
        ]

        expected_result = [
            {"rule": {"uid": "6"}, "package": {"name": "Isonet"}},
            {"rule": {"uid": "2"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "4"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "5"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "7"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
            {"rule": {"uid": "3"}, "package": {"name": "Standard"}},
        ]

        # Act
        result = RI.order_by_package_name(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    def test_orderByPackageName_when_oneOfEachExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
            {"rule": {"uid": "4"}, "package": {"name": "Premium"}},
        ]

        expected_result = [
            {"rule": {"uid": "4"}, "package": {"name": "Premium"}},
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
        ]

        # Act
        result = RI.order_by_package_name(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    def test_orderByPackageName_when_oneExists(self):
        # Arrange
        response_sample = [
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
        ]

        expected_result = [
            {"rule": {"uid": "1"}, "package": {"name": "Standard"}},
        ]

        # Act
        result = RI.order_by_package_name(response_sample)

        # Assert
        self.assertEqual(result, expected_result)

    def test_orderByPackageName_when_noneExists(self):
        # Arrange
        response_sample = []

        expected_result = []

        # Act
        result = RI.order_by_package_name(response_sample)

        # Assert
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
