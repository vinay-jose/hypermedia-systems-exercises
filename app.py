from flask import Flask, redirect, render_template, flash

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    search = requests.args.get("q")
    if search:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set)

@app.get("/contacts/new")
def contacts_new_get():
    return render_template("new.html", contact=Contact())

@app.post("/contacts/new")
def contacts_new_post():
    c = Contact(
        None,
        request.form['first_name'],
        request.form['last_name'],
        request.form['phone'],
        request.form['email']
    )
    if c.save():
        flash("Created New Contact!")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="7860")