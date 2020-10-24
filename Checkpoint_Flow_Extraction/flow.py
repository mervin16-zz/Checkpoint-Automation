class RuleIntermediator:
    @staticmethod
    def fetch_rules(object_name, filtered_list):
        access_rules_uid = []
        rules = []
        current_policy_processing = None

        # If list is not empty, proceed
        for rule in filtered_list:

            # Get the policy name
            policy = rule["package"]["name"]

            # Flag the current policy to
            # know when to switch
            if current_policy_processing is None:
                current_policy_processing = policy

            # If policy name has changed
            if current_policy_processing != policy:

                # Create new rule object and assign data
                rl = Rule(object_name, current_policy_processing, [])
                rl.access_rules_uid.extend(access_rules_uid)
                rules.append(rl)
                # Change old policy name to new
                current_policy_processing = policy

                # Clear uid array
                access_rules_uid.clear()

            access_rules_uid.append(rule["rule"]["uid"])

        if access_rules_uid:

            # This is to add the last item
            # Create new rule object and assign data
            rl = Rule(object_name, current_policy_processing, [])
            rl.access_rules_uid.extend(access_rules_uid)
            rules.append(rl)

            # Cleanup
            # Change old policy name to none
            current_policy_processing = None

            # Clear uid array
            access_rules_uid.clear()

        return rules

    @staticmethod
    def filter_layer_type(rule_list):
        return list(filter(lambda d: d["layer"]["type"] == "access-layer", rule_list))

    @staticmethod
    def order_by_package_name(rule_list):
        return sorted(rule_list, key=lambda k: k["package"]["name"])


class Rule:

    # Constructor
    def __init__(self, main_object_query, policy, access_rules_uid):
        self.main_object_query = main_object_query  # The object name we are querying
        self.policy = policy  # The policy this rule has been installed on
        self.access_rules_uid = (
            access_rules_uid  # A list of access rules uid on this policy
        )


class AccessRule:

    # Constructor
    def __init__(self, uid, name, source, destination, services, action, comment):
        self.uid = uid  # The rule UID
        self.name = name  # The rule name
        self.source = source  # The source ip address(es)
        self.destination = destination  # The destination ip address(es)
        self.services = services  # The port(s) in the rule
        self.action = action  # The action of the rule
        self.comment = comment  # The comment of the rule

