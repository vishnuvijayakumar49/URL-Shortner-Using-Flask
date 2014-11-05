from flask import *
import sqlite3
import random
# table columns 1.user_url,2.shorted

app=Flask(__name__)
 
@app.route("/" ,methods=['GET','POST'])
def shortner():
	if request.method=='POST':
		db=sqlite3.connect('url.db')
		cur=db.execute('''SELECT * from list where user_url=?''',(request.form['user_url'],))
		data=cur.fetchall()
		if data != []:
			short_url=data[0][1]
			cur=db.execute('''select * from list''' )
			short = [dict(user_url=row[0],shortened=row[1]) for row in cur.fetchall()]
			return render_template('shortn.html',short=short)
			
		else:
			short_url=str(random_string(5))
			db.execute('''insert into list values (?,?)''',[request.form['user_url'],short_url])
			db.commit()
			cur=db.execute('''select * from list''' )
			short = [dict(user_url=row[0],shortened=row[1]) for row in cur.fetchall()]
			return render_template('shortn.html',short=short)
	db=sqlite3.connect('url.db')	
	cur=db.execute('''select * from list''' )
	short = [dict(user_url=row[0],shortened=row[1]) for row in cur.fetchall()]
	return render_template('shortn.html',short=short)

@app.route("/<url>")
def direct(url=None):
	db=sqlite3.connect('url.db')
	cur=db.execute('''select * from list where shorted=?''',(url,))
	data=cur.fetchall()
	if data !=[]:
		org_url=data[0][0]
		return redirect(org_url,code=302)
	else:
		return render_template('error.html',url=url)

def random_string(length=5):
 possibles = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
 return ''.join(random.choice(possibles) for i in range(0, length))




app.run(debug=True)
