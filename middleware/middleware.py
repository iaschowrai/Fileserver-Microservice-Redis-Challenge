from flask import Flask, request, jsonify
import requests
import redis

app = Flask(__name__)

# Define the Redis client
r = redis.Redis(host='redis', port=6379)

# Define the file server URL
FILE_SERVER_URL = "http://file_server:1234/api/fileserver/"

# Endpoint to add a new file to the file server
@app.route("/api/fileserver/<string:filename>", methods=["PUT"])
def add_file(filename):
    # Save the file to the file server
    file_data = request.data
    response = requests.put(FILE_SERVER_URL + filename, data=file_data)
    
    # If the file was successfully saved to the file server, add it to the cache
    if response.status_code == 200:
        # Add the file to cache
        r.set(filename, file_data)
        # Set an expiration time for the cached file
        r.expire(filename, 3600)
    
    return response.content, response.status_code

# Endpoint to retrieve the contents of a file
@app.route("/api/fileserver/<string:filename>", methods=["GET"])
def get_file(filename):
    # Check if the file is in cache
    file_data = r.get(filename)
    if file_data:
        return file_data, 200
    # If the file is not in cache, retrieve it from the file server and add it to the cache
    else:
        response = requests.get(FILE_SERVER_URL + filename)
        if response.status_code == 200:
            file_data = response.content
            # Add the file to cache
            r.set(filename, file_data)
            # Set an expiration time for the cached file
            r.expire(filename, 3600)
            return file_data, 200
        else:
            return "", response.status_code

# Endpoint to delete a file
@app.route("/api/fileserver/<string:filename>", methods=["DELETE"])
def delete_file(filename):
    # Delete the file from the file server
    response = requests.delete(FILE_SERVER_URL + filename)
    # If the file was successfully deleted from the file server, remove it from the cache
    if response.status_code == 200:
        r.delete(filename)
    return response.content, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
