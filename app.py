from flask import Flask, redirect, render_template, flash, request
from models import Contact

Contact.load_db()
app = Flask(__name__)

app.secret_key = b'just keep swimming'

@app.get("/")
def index():
    return redirect("/contacts")

@app.get("/contacts")
def contacts():
    search = request.args.get("q")
    if search:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set)

@app.get("/contacts/<contact_id>")
def contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("show.html", contact=contact)

@app.get("/contacts/new")
def contacts_new_get():
    return render_template("new.html", contact=Contact())

@app.post("/contacts/new")
def contacts_new_post():
    c = Contact(
        None,
        request.form['first'],
        request.form['last'],
        request.form['phone'],
        request.form['email']
    )
    if c.save():
        flash("Created New Contact!")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)
    
@app.get("/contacts/<contact_id>/edit")
def contacts_edit_get(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)

@app.post("/contacts/<contact_id>/edit")
def contacts_edit_post(contact_id=0):
    c = Contact.find(contact_id)
    c.update(
        request.form['first'],
        request.form['last'],
        request.form['phone'],
        request.form['email']
    )
    if c.save():
        flash("Updated Contact!")
        return redirect(f"contacts/{str(contact_id)}")
    else:
        render_template("edit.html", contact=c)
        
@app.post("/contacts/<contact_id>/delete")
def contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    flash("Deleted Contact!")
    return redirect("/contacts")
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="7860", debug=True)