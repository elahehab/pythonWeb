from flask import Flask
from flask import request
import pymysql

app = Flask(__name__)

@app.route('/addStrategies', methods=['GET', 'POST'])
def addStrategies():
    strategies = str(request.form.get("strategies")).split(",")
    playerEmail = request.form.get("playerEmail")
    partId = request.form.get("partId")
    write_strategy_to_db(playerEmail, partId, strategies)

    return "Strategies added"

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    email = request.form.get("email")
    write_user_data_to_db(email)

    return "User added"

	
@app.route('/test')
def test():
	print "testing..."
	return "hello!"


def write_strategy_to_db(playerEmail, partId, strategies):
    db = pymysql.connect("localhost", "root", "root", "thesiscloud")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    for i in range(0, len(strategies)):

        # Prepare SQL query to INSERT a record into the database.
        sql = """INSERT INTO strategy(strategyId, partId, playerId)
                 select """ + strategies[i] + """,""" + partId + """, id from player where email=\'""" + playerEmail + """\' limit 1"""
        print sql
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

    # disconnect from server
    db.close()


def write_user_data_to_db(email):
    db = pymysql.connect("localhost", "root", "root", "thesiscloud")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()


    # Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO player(email)
             VALUES (\'""" + email + """\')"""
    print sql
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()

if __name__ == "__main__":
    app.run()