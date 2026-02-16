from flask import Flask, flash, render_template, redirect, url_for, request, session
from config import Config
from extensions import db
from forms import LoginForm, PostForm
from models import Post, Category

app = Flask(__name__)
app.config.from_object(Config)


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

db.init_app(app)

@app.route("/")
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["admin"] = True
            flash("Welcome admin!", "success")
            return redirect(url_for("index"))

        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login")) 

    return render_template("login.html")  

@app.route("/create", methods=["GET", "POST"])
def create_post():

    if not session.get("admin"):
        return redirect(url_for("login"))

    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            author=form.author.data,
            content=form.content.data,
            category_id=form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash("Post published successfully", "success")
        return redirect(url_for("index"))

    return render_template("create.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):

    if not session.get("admin"):
        return redirect(url_for("login"))

    post = Post.query.get_or_404(id)

    form = PostForm(obj=post)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.content = form.content.data
        post.category_id = form.category.data

        db.session.commit()
        return redirect(url_for("post", id=post.id))

    form.category.data = post.category_id
    return render_template("edit.html", form=form)

@app.route("/delete/<int:id>")
def delete_post(id):

    if not session.get("admin"):
        return redirect(url_for("login"))

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted", "warning")
    return redirect(url_for("index"))

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        flash("Please enter a search term", "warning")
        return redirect(url_for("index"))
    posts = Post.query.filter(Post.title.ilike(f"%{query}%")).all()
    if not posts:
        flash("No posts found", "danger")
    return render_template("index.html", posts=posts, category_name=f"Search: {query}")

@app.route("/category/<int:id>")
def category(id):
    category = Category.query.get_or_404(id)
    posts = Post.query.filter_by(category_id=id).order_by(Post.date.desc()).all()
    posts = Post.query.filter_by(category=category).all()

    if not posts:
        flash("No posts in this category yet", "warning")
    
    return render_template("index.html", posts=posts, category_name=category.name)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))

@app.context_processor
def inject_categories():
    return dict(Category=Category)

if __name__ == "__main__":
    app.run(debug=True)