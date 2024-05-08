from app import app

if __name__ == "__main__":
    app.run(debug=True)



# flask run - to run the app
# flask db init - to initialize the database
# flask db migrate -m "Initial" - to create the migration
# flask db upgrade - to apply the migration
# flask db downgrade - to undo the migration
# flask shell - to open the shell
