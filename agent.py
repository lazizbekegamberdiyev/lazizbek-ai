class AgentState:
    def __init__(self, goal):
        self.goal = goal
        self.actions = []
        self.tool_results = []
        self.final_answer = None

    def add_action(self, action):
        self.actions.append(action)

    def add_tool_result(self, result):
        self.tool_results.append(result)

    def set_final_answer(self, answer):
        self.final_answer = answer
