from flask import Flask , render_template , request,redirect
import os
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import time


currentdir = os.path.dirname(os.path.abspath(__file__))

 
app = Flask(__name__)
uInfo = dict()


@app.route("/" , methods = ["GET"])
def home():
    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT DISTINCT(Country)from user"
    cities = c.execute(query).fetchall()
    c.close()

    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT petID,petName , imgName from pet JOIN image on pet.petID = image.pet_id LIMIT  3"
    cur = c.execute(query)
    result = [dict(petID =row[0],petName=row[1], imgName=row[2]) for row in cur.fetchall()]

    return render_template("Home.html",result = result,cities = cities)
            

@app.route("/home" , methods = ["GET" , "POST"])
def signup():
    if request.method == "GET":
        return redirect("/")
    else:
        first = request.form.get('Fname')
        last = request.form.get('Lname')
        password = request.form.get('pass')
        mail = request.form.get('email')
        City = request.form.get('city')
        phone = request.form.get('phone')
        addresss = request.form.get('address')

        Hashed_password = generate_password_hash(password)
        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
    
        query = "INSERT INTO user (Fname,Lname,Country,email,pass,phone,address)  VALUES ('{first}','{last}','{City}','{mail}','{password}','{phone}','{address}' )".format(
            first =first , last = last ,City = City , mail= mail, password = Hashed_password , phone=phone , address = addresss)
        c.execute(query)
    # Save (commit) the changes
        conn.commit()
        conn.close()
        
        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "SELECT DISTINCT(Country)from user"
        cities = c.execute(query).fetchall()
        c.close()

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "SELECT petID,petName , imgName from pet JOIN image on pet.petID = image.pet_id LIMIT  3"
        cur = c.execute(query)
        result = [dict(petID =row[0],petName=row[1], imgName=row[2]) for row in cur.fetchall()]
        time.sleep(0.3)
        return render_template("Home.html",result = result,cities = cities)

@app.route("/signin" , methods = ["GET","POST"])
def signin():
    if request.method == "GET":
        return render_template("Home.html")
    else:
        Email = request.form.get('mail')
        password = request.form.get('pass')
        #########################################
        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
    
        query = "select * from user where email = '{mail}'".format(mail = Email)
        result = c.execute(query).fetchall()
        if len(result) != 1 :
            return render_template("Error.html",name = "not_signed_up.png")
        else:
            for res in result:
                uInfo["ID"] = res[0]
                uInfo["fname"] = res[1]
                uInfo["lname"] = res[2]
                uInfo["city"] = res[3]
                uInfo["mail"] = res[4]
                uInfo["pass"] = res[5]
                uInfo["phone"] = res[6]
                uInfo["address"] = res[7]

            if not check_password_hash(uInfo["pass"], password):
                return render_template("Error.html",name="Wrong_email_or_password.png")
            else:
                return redirect("/profile")


        
        return render_template("home.html")
       

@app.route("/profile" , methods = ["GET","POST"])
def profile():
    userName = uInfo["fname"] + " " +uInfo["lname"]

    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    
    query = "select * from user where id = '{ID}'".format(ID = uInfo["ID"])
    result = c.execute(query).fetchall()
    if len(result) != 1 :
        return render_template("Error.html",name = "not_signed_up.png")
    else:
        for res in result:
            uInfo["ID"] = res[0]
            uInfo["fname"] = res[1]
            uInfo["lname"] = res[2]
            uInfo["city"] = res[3]
            uInfo["mail"] = res[4]
            uInfo["pass"] = res[5]
            uInfo["phone"] = res[6]
            uInfo["address"] = res[7]


    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT DISTINCT(Country)from user"
    cities = c.execute(query).fetchall()
    c.close()


    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT petID,petName , imgName from pet JOIN image on pet.petID = image.pet_id LIMIT  3"
    cur = c.execute(query)
    result = [dict(petID =row[0],petName=row[1], imgName=row[2]) for row in cur.fetchall()]
    return render_template("profile.html", userName = userName , result = result ,cities = cities)


@app.route("/info" , methods = ["GET","POST"])
def info():
    if request.method == "GET":
        userName = uInfo["fname"] + " " +uInfo["lname"]
        return render_template("AccountInfo.html", uInfo = uInfo ,userName = userName)
    else:
        aftermail = request.form.get("email")
        afterphone = request.form.get("phone")
        afteraddress = request.form.get("address")
        aftercity = request.form.get("city")
        oldpass = request.form.get("oldpass")
        if not check_password_hash(uInfo["pass"],oldpass):
                return render_template("Error.html",name = "password_is_wrong.png")
        else:
            conn = sqlite3.connect(currentdir + "\\users.db")
            c = conn.cursor()
            query = "update user set email = '{mail}' , phone = '{phone}' , address = '{address}' , Country = '{city}'  where id = {ID} ".format(mail = aftermail , phone = afterphone , address = afteraddress , city = aftercity , ID =  uInfo["ID"]) 
            c.execute(query)
            # Save (commit) the changes
            conn.commit()
            conn.close()
            time.sleep(0.3)
            return redirect("/profile")



@app.route("/addpet" , methods = ["GET","POST"])
def addpet():
    userName = uInfo["fname"] + " " +uInfo["lname"]
    return render_template("addPet.html", userName = userName)


@app.route("/added" , methods = ["GET","POST"])
def added():
    if request.method == "POST":
        petType = request.form.get("type")
        Name = request.form.get("petName")
        gender = request.form.get("gender")
        color = request.form.get("color")
        age = request.form.get("age")
        size = request.form.get("size")
        breed = request.form.get("breed")

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "insert into pet (petName,age,gender,color,size,type,breed,user_id) values('{petname}','{petage}','{petgender}','{petcolor}','{petsize}','{petype}','{petbreed}',{uID}) ".format(petname = Name , petage = age , petgender = gender , 
        petcolor = color ,petsize = size , petype = petType , petbreed = breed, uID =  uInfo["ID"]) 
        c.execute(query)
        # Save (commit) the changes
        conn.commit()
        conn.close()

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "select max(petID) from pet" 
        petID = c.execute(query).fetchall()[0][0]
        conn.close()
       
        file = request.files["file"]
        OSpath = os.path.join("C:\\Users\\emadh\\Desktop\\pets\\static",file.filename)
        file.save(OSpath)

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "insert into image (imgName , pet_id) values ('{imgname}' , {petID})".format(imgname = file.filename ,petID = petID )
        c.execute(query)
        # Save (commit) the changes
        conn.commit()
        conn.close()
        time.sleep(0.3)
        return redirect("/profile")

    
    return redirect("/")


@app.route("/petInfo" , methods = ["GET","POST"])
def petInfo():
    petID = request.form.get("pet")
    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT * from pet where petID = {ID}".format(ID = petID)
    cur = c.execute(query)
    petinfo = [dict(petID =row[0],petName=row[1], age=row[2],gender =row[3],color=row[4],size = row[5],typee= row[6] ,breed =row[7],uID=row[8]) for row in cur.fetchall()]
    conn.close()

    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT imgName from image where pet_id = {ID}".format(ID = petID)
    nameImg = c.execute(query).fetchall()[0][0]
    conn.close()

    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "   SELECT email , phone ,Country,address from user where id = {ID}".format(ID = petinfo[0]["uID"])
    cur = c.execute(query)
    ownerinfo = [dict(email =row[0],phone=row[1], city=row[2],address =row[3]) for row in cur.fetchall()]
    conn.close()
    if not uInfo:
        return render_template("petinfoNoTlogged.html",petinfo = petinfo , nameImg = nameImg ,ownerinfo = ownerinfo )
    else:
        userName = uInfo["fname"] + " " +uInfo["lname"]
        return render_template("petInfoLogged.html",userName = userName ,petinfo = petinfo , nameImg = nameImg ,ownerinfo = ownerinfo )



@app.route("/gallery" , methods = ["GET","POST"])
def gall():
    selectedCity = request.form.get("city")
    if request.form.get("dog") == None:
        selectedType = request.form.get("cat")
    else:
        selectedType = request.form.get("dog")
    
    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT petID, petName , imgName from pet JOIN image on pet.petID = image.pet_id JOIN user on pet.user_id = user.id where user.Country = '{country}' and pet.type ='{type}' ".format(country = selectedCity ,type =  selectedType)
    cur = c.execute(query)
    galleryItems = [dict(petID =row[0],petName=row[1], imgName=row[2]) for row in cur.fetchall()]
    conn.close()
    if not uInfo:
        return render_template("galleryNoTlogged.html",galleryItems = galleryItems)
    else:
        userName = uInfo["fname"] + " " +uInfo["lname"]
        return render_template("galleryLogged.html",userName = userName ,galleryItems = galleryItems)





@app.route("/editPets" , methods = ["GET","POST"])
def editpets():
    conn = sqlite3.connect(currentdir + "\\users.db")
    c = conn.cursor()
    query = "SELECT *  from pet where user_id = {ID} ".format(ID = uInfo["ID"])
    cur = c.execute(query)
    pets = [dict(petID =row[0],petName=row[1], age=row[2], gender=row[3], color=row[4], size=row[5], type=row[6] , breed = row[7]) for row in cur.fetchall()]
    conn.close()
    userName = uInfo["fname"] + " " +uInfo["lname"]
    return render_template("editPets.html" , userName = userName , pets=pets)

@app.route("/edited" , methods = ["GET","POST"])
def edited():
        petID = request.form.get("delete")

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "select imgName from image where pet_id = {ID} ".format(ID = petID)
        imgName = c.execute(query).fetchall()[0][0]
        conn.close()

        OSpath = os.path.join("C:\\Users\\emadh\\Desktop\\pets\\static",imgName)
        if os.path.exists(OSpath):
            os.remove(OSpath)


        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "delete from image where pet_id = {ID} ".format(ID = petID)
        cur = c.execute(query)
        conn.commit()
        conn.close()

        conn = sqlite3.connect(currentdir + "\\users.db")
        c = conn.cursor()
        query = "delete from pet where petID = {ID} ".format(ID = petID)
        cur = c.execute(query)
        conn.commit()
        conn.close()
        time.sleep(0.3)
        return redirect("/profile")



   

    



@app.route("/logout" , methods = ["GET","POST"])
def out():
    uInfo.clear()
    return redirect("/")

        
        
 