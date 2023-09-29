from flask import Flask

from src import status

app = Flask(__name__)

COUNTERS = {}

# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message":f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

#Create a route for method PUT on endpoint /counters/<name>
@app.route('/counters/<name>', methods=['PUT'])
#Create a function to implement that route
def update_counter(name):
    #Increment the counter by 1
    COUNTERS[name] += 1
    #Return the new counter and a 200_OK return code
    return{name: COUNTERS[name]}, status.HTTP_200_OK

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    if name in COUNTERS:
        return{name: COUNTERS[name]}, status.HTTP_200_OK
    else:
        return {},status.HTTP_404_NOT_FOUND
@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    del COUNTERS[name]
    return {}, status.HTTP_204_NO_CONTENT