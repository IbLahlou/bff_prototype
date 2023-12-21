from flask import Flask, render_template, jsonify
from flask_graphql import GraphQLView
from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define a simple GraphQL schema
query_type = GraphQLObjectType(
    name='RootQueryType',
    fields={
        'message': GraphQLField(
            type_=GraphQLString,
            resolver=lambda obj, info: 'Hello from Service 1!'
        ),
        'custom_data': GraphQLField(
            type_=GraphQLString,
            resolver=lambda obj, info: get_custom_data()
        )
    }
)

schema = GraphQLSchema(query=query_type)

# Add the GraphQL endpoint to the Flask app
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
