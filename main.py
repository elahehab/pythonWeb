from flask import *
import pymysql

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('instructions.html')

@app.route('/gameInstruction', methods=['GET', 'POST'])
def show_game_instruction():
    return render_template('game_instruction.html')

@app.route('/researchInstruction', methods=['GET', 'POST'])
def show_research_instruction():
    return render_template('research_instruction.html')

@app.route('/play', methods=['POST'])
def play():
    return render_template('play.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/finish', methods=['POST'])
def finish():
    if(current_email == "" or current_email == None):
        print current_email
        return "invalid email address"
    else:
        print current_email
    sex = request.form.get("sex")
    age = request.form.get("age")
    education = request.form.get("education")
    game_time_in_day = request.form.get("game_time_in_day")
    since_year = request.form.get("since_year")
    game_platform = request.form.get("game_platform")
    game_like_level = request.form.get("game_like_level")
    help_personal_abilities = request.form.get("help_personal_abilities")
    improve_performance = request.form.get("improve_performance")
    change_strategy = request.form.get("change_strategy")
    return render_template('end.html')

@app.route('/addStrategies', methods=['GET', 'POST'])
def add_strategies():
    strategies = str(request.form.get("strategies")).split(",")
    playerEmail = request.form.get("playerEmail")
    partId = request.form.get("partId")
    write_strategy_to_db(playerEmail, partId, strategies)

    return "Strategies added"

@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    email = request.form.get("email")
    
    result = write_user_data_to_db(email)
    print "result is ", str(result)
    return str(result)

	
@app.route('/addGameData', methods=['GET', 'POST'])
def add_game_data():
    email = request.form.get("email")
    data = request.form.get("data")
    file = open("results/"+email+".txt", "a")
    file.write(data)
    file.write("\n")
    file.close()
    return "ok"


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
    sql = """INSERT INTO player(email) select * from (select \'""" + email + """\') as tmp where not exists 
    (select email from player where email=\'""" + email + """\') limit 1"""

    print sql
    
    result = True
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        result = False

    # disconnect from server
    db.close()
    return result

def write_user_personal_data_to_db(sex, age, education, game_time_in_day,
 since_year, game_platform, game_like_level, help_personal_abilities,
  improve_performance, change_strategy):
    print "hello :)"


if __name__ == "__main__":
    app.run()