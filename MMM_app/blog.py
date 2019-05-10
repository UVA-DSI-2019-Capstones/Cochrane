from flask import Blueprint, render_template, request
from mysite import db

bp = Blueprint("blog", __name__)

# Main page
@bp.route("/")
def main_page():
    return render_template("main.html")

# Cochrane to Wikipedia page
@bp.route("/coch_to_wiki")
def coch_wiki_page():
    instruction = ["Please input a Cochrane Review.",
                   "For example, Abstinence-plus programs for HIV " +\
                   "infection prevention in high-income countries.\n",
                   "If the review is not found, " +\
                   "a list of similar reviews will be returned."]
    return render_template("coch_to_wiki.html", instruction = instruction)

# Wikipedia to Cochrane page
@bp.route("/wiki_to_coch")
def wiki_coch_page():
    instruction = ["Please input a Wikipedia article",
                   "For example, Weight management.",
                   "If the article is not found, " +\
                   "A list of similar articles will be returned."]
    return render_template("wiki_to_coch.html", instruction = instruction)

# Cochrane-to-Wikipedia page after submission
@bp.route("/coch_to_wiki", methods=["POST"])
def search_wiki():
    if request.method == "POST":
        review = request.form["review"]

        if len(review) > 0:
            database = db.get_db()

            sql = "SELECT wiki, accuracy FROM coch_wiki " +\
                  "WHERE coch ='" + review + "'" +\
                  "ORDER BY accuracy DESC;"
            result = database.execute(sql).fetchall()

            if len(result) > 0: # At least one row is returned
                article = [row[0] for row in result]
                similarity = [row[1] for row in result]
                similarity = ["missing" if item == None else item \
                              for item in similarity]
                return render_template("coch_to_wiki2.html",
                                       review = review,
                                       result = zip(article, similarity))
            else:
                sql = "SELECT DISTINCT coch FROM coch_wiki " +\
                      "WHERE coch LIKE '%" + review + "%';"
                result = database.execute(sql).fetchall()

                if len(result) > 0:
                    review_list = [row[0] for row in result]
                    return render_template("coch_to_wiki3.html",
                                           review_list = review_list)
                else:
                    instruction = ["No Similar Cochrane Reviews found.",
                                   "Please input a new one."]
                    return render_template("coch_to_wiki.html",
                                           instruction = instruction)
        else:
            instruction = ["No input found.",
                           "Please input a Cochrane review."]
            return render_template("coch_to_wiki.html",
                                   instruction = instruction)

# Wikipedia to Cochrane page after submission
@bp.route("/wiki_to_coch", methods=["POST"])
def search_coch():
    if request.method == "POST":
        article = request.form["article"]

        if len(article) > 0:
            database = db.get_db()

            sql = "SELECT coch, accuracy FROM wiki_coch " +\
                  "WHERE wiki='" + article + "'" +\
                  "ORDER BY accuracy DESC;"
            result = database.execute(sql).fetchall()

            if len(result) > 0:
                review = [row[0] for row in result]
                similarity = [row[1] for row in result]
                similarity = ["Missing" if item == None else item \
                              for item in similarity]
                return render_template("wiki_to_coch2.html",
                                       article = article,
                                       result = zip(review, similarity))
            else:
                sql = "SELECT DISTINCT wiki FROM wiki_coch " +\
                      "WHERE wiki LIKE '%" + article + "%';"
                result = database.execute(sql).fetchall()

                if len(result) > 0:
                    article_list = [row[0] for row in result]
                    return render_template("wiki_to_coch3.html",
                                           article_list = article_list)
                else:
                    instruction = ["No Similar Wikipedia article found.",
                                   "Please input a new one."]
                    return render_template("wiki_to_coch.html",
                                           instruction = instruction)
        else:
            instruction = ["No input found.",
                           "Please input a Wikipedia article."]
            return render_template("wiki_to_coch.html",
                                   instruction = instruction)