from backend.extensions import db


class DashboardQueryResult(db.Model):
    """DashboardQueryResult model"""

    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text)
    chatgpt_gql = db.Column(db.Text)
    subgraph = db.Column(db.Text)
    chain = db.Column(db.Text, default="ethereum")
    gql_valid = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return "<DashboardQueryResult %s>" % self.user_input

    def to_dict(self):
        return {
            "id": self.id,
            "user_input": self.user_input,
            "chatgpt_gql": self.chatgpt_gql,
            "subgraph": self.subgraph,
            "chain": self.chain,
            "user_id": self.user_id,
        }
