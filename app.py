
from cs50 import SQL
from flask import Flask, render_template, request
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set

db = SQL("sqlite:///waits.db")



@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/search/', methods=["GET", "POST"])
def search():
    # get the data needed to populate the selection options in the form
    dates = db.execute("SELECT DISTINCT quarterending FROM docwmar23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hbt FROM docwmar23) ORDER BY hbname")
    pttyp = db.execute("SELECT DISTINCT patienttype FROM docwmar23")
    specialty = db.execute("SELECT * FROM specialtyref WHERE specialty1 IN (SELECT DISTINCT specialty FROM docwmar23) ORDER BY SpecialtyName")
    gumpy = "visibility: hidden;"

    if request.method == "POST":
        # Get what the user selected in the form
        gumpy = "visibility: visible;"
        selsorc = request.form.get("sorc")
        seldates = request.form.get("dates")
        selhb = request.form.get("hb")
        selpttyp = request.form.get("pttyp")
        selspecialty = request.form.get("specialty")
        # need a blank to insert into fstring
        blank = ""
        # write sqlite queary into an fstring
        queary = f"SELECT *, hbref.hbname, specialtyref.specialtyname, cwmar23.numberofwaits, cwmar23.over12weeks, cwmar23.median, cwmar23.w90thpercentile FROM docwmar23 JOIN cwmar23 ON docwmar23.quarterending = cwmar23.monthending AND docwmar23.hbt = cwmar23.hbt1 AND docwmar23.patienttype = cwmar23.patienttype1 AND docwmar23.specialty = cwmar23.specialty1 JOIN hbref ON docwmar23.hbt = hbref.hb1 JOIN specialtyref ON docwmar23.specialty = specialtyref.specialty1 WHERE numberofwaits != \"{blank}\" AND quarterending IS {seldates} AND hbt IS {selhb} AND patienttype IS {selpttyp} AND specialty IS {selspecialty} ORDER BY hbname, SpecialtyName"
        # execute queary
        data = db.execute(queary)
        # load a diferent webpage depending on if user wanted more or less detailed info
        if selsorc == "cwmar23":
            return render_template('search.html', dates=dates, hb=hb, pttyp=pttyp, specialty=specialty, data=data, gumpy=gumpy)

        if selsorc == "docwmar23":
            return render_template('searchc.html', dates=dates, hb=hb, pttyp=pttyp, specialty=specialty, data=data, gumpy=gumpy)


    else:

       return render_template('search.html', dates=dates, hb=hb, pttyp=pttyp, specialty=specialty, gumpy=gumpy)


@app.route('/select/', methods=["GET", "POST"])
def select():

    if request.method == "POST":
        return render_template('search.html')

    else:

       return render_template('select.html')


@app.route('/psy/', methods=["GET", "POST"])
def psy():

    months = db.execute("SELECT DISTINCT month FROM psyseenmar23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hb FROM psyseenmar23) ORDER BY hbname")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        selsorw = request.form.get("sorw")

        blank = ""
        # run if user wants info on completed waits
        if selsorw == 'psyseenmar23':
            queary = f"SELECT *, hbref.hbname FROM psyseenmar23 JOIN hbref ON psyseenmar23.hb = hbref.hb1 WHERE totalpatientsseen != \"{blank}\" AND month IS {selmonth} AND hb IS {selhb} ORDER BY hbname"

            data = db.execute(queary)
            return render_template('psy.html', months=months, hb=hb, data=data, gumpy=gumpy)
        # run if user wants info on ongoing waits
        if selsorw == 'psywaitmar23':
            queary = f"SELECT *, hbref.hbname FROM psywaitmar23 JOIN hbref ON psywaitmar23.hb = hbref.hb1 WHERE totalpatientswaiting != \"{blank}\" AND month IS {selmonth} AND hb IS {selhb} ORDER BY hbname"

            data = db.execute(queary)
            return render_template('psywait.html', months=months, hb=hb, data=data, gumpy=gumpy)
        #reload page if no selection made
        return render_template('psy.html', months=months, hb=hb, gumpy=gumpy)

    else:
        return render_template('psy.html', months=months, hb=hb, gumpy=gumpy)


@app.route('/camh/', methods=["GET", "POST"])
def camh():

    months = db.execute("SELECT DISTINCT month FROM camhseenmar23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hb FROM camhseenmar23) ORDER BY hbname")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        selsorw = request.form.get("sorw")

        blank = ""
        # run if user wants info on completed waits
        if selsorw == 'camhseenmar23':
            queary = f"SELECT *, hbref.hbname FROM camhseenmar23 JOIN hbref ON camhseenmar23.hb = hbref.hb1 WHERE totalpatientsseen != \"{blank}\" AND month IS {selmonth} AND hb IS {selhb} ORDER BY hbname"

            data = db.execute(queary)
            return render_template('camhseen.html', months=months, hb=hb, data=data, gumpy=gumpy)
        # run if user wants info on ongoing waits
        if selsorw == 'camhwaitmar23':
            queary = f"SELECT *, hbref.hbname FROM camhwaitmar23 JOIN hbref ON camhwaitmar23.hb = hbref.hb1 WHERE totalpatientswaiting != \"{blank}\" AND month IS {selmonth} AND hb IS {selhb} ORDER BY hbname"

            data = db.execute(queary)
            return render_template('camhwait.html', months=months, hb=hb, data=data, gumpy=gumpy)
        #reload page if no selection made
        return render_template('camhseen.html', months=months, hb=hb, gumpy=gumpy)

    else:
        return render_template('camhseen.html', months=months, hb=hb, gumpy=gumpy)



@app.route('/diag/', methods=["GET", "POST"])
def diag():

    months = db.execute("SELECT DISTINCT monthending FROM diagmar23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hbt FROM diagmar23) ORDER BY hbname")
    spectest = db.execute("SELECT DISTINCT diagnostictestdescription FROM diagmar23")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        seltest = request.form.get("spectest")
        blank = ""

        # First queary is to gather all information that i will need
        queary = f"SELECT *, hbref.hbname FROM diagmar23 JOIN hbref ON diagmar23.hbt = hbref.hb1 WHERE numberonlist != \"{blank}\" AND monthending IS {selmonth} AND hbt IS {selhb} AND diagnostictestdescription IS {seltest} ORDER BY hbname, diagnostictesttype, diagnostictestdescription, cast(waitingtime as unsigned)"
        data = db.execute(queary)
        # second queary is to create a dataset that is only the ittles i want for each row
        q2 = f"SELECT DISTINCT monthending, hbt, diagnostictesttype, diagnostictestdescription, hbref.hbname FROM diagmar23 JOIN hbref ON diagmar23.hbt = hbref.hb1 WHERE numberonlist != \"{blank}\" AND monthending IS {selmonth} AND hbt IS {selhb} AND diagnostictestdescription IS {seltest} ORDER BY hbname, diagnostictesttype, diagnostictestdescription, cast(waitingtime as unsigned)"
        titles = db.execute(q2)

        # Because this database has information on multiple rows that i want to display ona single row. here i am adding that data so that it exists on a single row
        # the list of rows in titles is the total number of rows i want
        for i in range(len(titles)):
            # q is an interger which will count the total number of patients waiting in each hb/specialty/date
            q = 0
            # there are 17 bits of information that is storred on different rows that i want on 1 row so i need to create 17 new columns and add them to the desired rows along with the data
            for j in range(17):
                q += int(data[j +i*17]["numberonlist"])
                titles[i][j] = data[j + i*17]["numberonlist"]
            titles[i]["total"] = q
        return render_template('diag.html', months=months, hb=hb, spectest=spectest, data=data, titles=titles, gumpy=gumpy)



    else:
        return render_template('diag.html', months=months, hb=hb, spectest=spectest, gumpy=gumpy)


@app.route('/mskseen/', methods=["GET", "POST"])
def mskseen():

    months = db.execute("SELECT DISTINCT quarter FROM mskseenmar23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hbt FROM mskseenmar23) ORDER BY hbname")
    specialty = db.execute("SELECT DISTINCT specialty FROM mskseenmar23")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        selspec = request.form.get("specialty")
        blank = ""

        queary = f"SELECT *, hbref.hbname FROM mskseenmar23 JOIN hbref ON mskseenmar23.hbt = hbref.hb1 WHERE patientsseen != \"{blank}\" AND quarter IS {selmonth} AND hbt IS {selhb} AND specialty IS {selspec} ORDER BY hbname"
        data = db.execute(queary)

        x = ['numberwhowaitedzerotofourweekspc', 'numberwhowaitedfivetoeightweekspc', 'numberwhowaitedninetotwelveweekspc', 'numberwhowaitedthirteentosixteenweekspc', 'numberwhowaitedsixteenplusweekspc', 'numberwhowaitedfourplusweekspc']

        for i in range(len(data)):
            for j in x:
                data[i][j] = round(float(data[i][j]), 1)

        return render_template('mskseen.html', months=months, hb=hb, specialty=specialty, data=data, gumpy=gumpy)

    else:

        return render_template('mskseen.html', months=months, hb=hb, specialty=specialty, gumpy=gumpy)






@app.route('/mskwait/', methods=["GET", "POST"])
def mskwait():


    months = db.execute("SELECT DISTINCT quarter FROM mskseenmar23")
    hb = db.execute ("SELECT DISTINCT hbname FROM hscpref WHERE hscp1 IN (SELECT DISTINCT hscp FROM mskwaitmar23) ORDER BY hbname")
    specialty = db.execute("SELECT DISTINCT specialty FROM mskwaitmar23")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        selspec = request.form.get("specialty")
        blank = ""

        queary = f"SELECT *, hscpref.hscpname FROM mskwaitmar23 JOIN hscpref ON mskwaitmar23.hscp = hscpref.hscp1 WHERE patientsseen != \"{blank}\" AND quarter IS {selmonth} AND hbname IS {selhb} AND specialty IS {selspec} ORDER BY hbname, specialty, hscpname"
        data = db.execute(queary)

        return render_template('mskwait.html', months=months, hb=hb, specialty=specialty, data=data, gumpy=gumpy)

    else:



        return render_template('mskwait.html', months=months, hb=hb, specialty=specialty, gumpy=gumpy)



@app.route('/ane/', methods=["GET", "POST"])
def ane():

    months = db.execute("SELECT DISTINCT month FROM aneaug23")
    hb = db.execute("SELECT * FROM hbref WHERE hb1 IN (SELECT DISTINCT hbt FROM aneaug23) ORDER BY hbname")
    location = db.execute("SELECT * FROM locationref WHERE location IN (SELECT DISTINCT treatmentlocation FROM aneaug23) ORDER BY locationname")
    department = db.execute("SELECT DISTINCT departmenttype FROM aneaug23")
    gumpy = "visibility: hidden;"

    if request.method == "POST":

        gumpy = "visibility: visible;"
        selmonth = request.form.get("month")
        selhb = request.form.get("hb")
        seldep = request.form.get("department")
        blank = ""

        queary = f"SELECT *, hbref.hbname, locationref.locationname FROM aneaug23 JOIN hbref ON aneaug23.hbt = hbref.hb1 JOIN locationref ON aneaug23.treatmentlocation = locationref.location WHERE numberofattendancesall != \"{blank}\" AND month IS {selmonth} AND hbt IS {selhb} AND departmenttype IS {seldep} ORDER BY hbname, locationname, departmenttype, month"
        data = db.execute(queary)


        return render_template('ane.html', months=months, hb=hb, location=location, department=department, data=data, gumpy=gumpy)

    else:
        return render_template('ane.html', months=months, hb=hb, location=location, department=department, gumpy=gumpy)