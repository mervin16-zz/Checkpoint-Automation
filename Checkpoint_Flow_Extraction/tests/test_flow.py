import unittest
from models.flow import RuleIntermediator as RI


class TestFlow(unittest.TestCase):

    ############################################################
    #################### Rule Intermediator ####################
    ############################################################

    def test_fetchRules_when_oneRuleExists(self):
        # Arrange
        filtered_list = [
            {
                "rule": {"uid": "4"},
                "layer": {"name": "Premium Network", "type": "access-layer"},
                "package": {"name": "Standard"},
            }
        ]

        expected_result = {"Standard": {"uids": ["4"], "layer": "Premium Network"}}

        # Act
        result = RI.fetch_rules(filtered_list)

        # Assert
        self.assertEqual(expected_result, result)

    def test_fetchRules_when_oneRuleEachPolicyExists(self):
        # Arrange
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

        expected_result = {
            "Standard": {"uids": ["4"], "layer": "Premium Network"},
            "Premium": {"uids": ["2"], "layer": "Premium Network"},
        }

        # Act
        result = RI.fetch_rules(filtered_list)

        # Assert
        self.assertEqual(result, expected_result)

    def test_fetchRules_when_multipleRulesExists(self):
        # Arrange
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

        expected_result = {
            "Standard": {"uids": ["4", "10"], "layer": "Premium Network"},
            "Premium": {"uids": ["2", "5", "78"], "layer": "Premium Network"},
        }

        # Act
        result = RI.fetch_rules(filtered_list)

        # Assert
        self.assertEqual(result, expected_result)

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
