from SLRtool import app

# def run(
#         host='0.0.0.0',
#         port=4000
# )

"""
Run RESTful API Server.
"""

# Return the app to the runner state so it gets actually loaded.
#   return app.run(host=host, port=port)


if __name__ == '__main__':
    app.debug = True
    app.run() #host='0.0.0.0', port=5000
    # if the app shall be visible in the local network use the following
    # app.run(host='0.0.0.0', port=5000)