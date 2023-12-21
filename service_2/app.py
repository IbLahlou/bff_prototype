from flask import Flask, render_template, jsonify
from flask_graphql import GraphQLView
from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString
import requests

app = Flask(__name__)

# Define a simple GraphQL schema
query_type = GraphQLObjectType(
    name='RootQueryType',
    fields={
        'message_from_service_1': GraphQLField(
            type_=GraphQLString,
            resolver=lambda obj, info: get_message_from_service_1()
        )
    }
)

schema = GraphQLSchema(query=query_type)

# Function to make a GraphQL request to service_1
def get_message_from_service_1():
    try:
        response = requests.post('http://localhost:5000/graphql', json={'query': '{ message }'})
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        message_from_service_1 = data['data']['message']
        print("Successfully obtained message from service_1:", message_from_service_1)
        return message_from_service_1
    except requests.RequestException as e:
        print("Error making request to service_1:", e)
        return "Error: Could not fetch message from service_1"

# Add the GraphQL endpoint to the Flask app
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(port=5002, debug=True)

