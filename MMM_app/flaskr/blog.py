from flask import (
    Blueprint, render_template, request
)
from flaskr import db

bp = Blueprint("blog", __name__)

@bp.route("/")
def main_page():
    return render_template("main.html")

@bp.route("/coch_to_wiki")
def coch_wiki_page():
    return render_template("coch_to_wiki.html")

@bp.route("/wiki_to_coch")
def wiki_coch_page():
    return render_template("wiki_to_coch.html")

@bp.route("/coch_to_wiki", methods=["POST"])
def search_wiki():
    if request.method == "POST":
        review = request.form["review"]
        doi = request.form["doi"]
        
        if len(doi) > 0 or len(review) > 0:
            database = db.get_db()
            
            if len(doi) > 0:
                sql = "SELECT doi, review, article, similarity FROM review_to_wiki WHERE doi LIKE '%"\
                      + doi + "%';"
                result = database.execute(sql).fetchall()
                
                if len(result) > 0: # One or more than one row is returned
                    doi = result[0][0]
                    review = result[0][1]
                    article = [row[2] for row in result]
                    similarity = [row[3] for row in result] 
                else:
                    doi = "The doi is not found"
                    review = ""
                    article = []
                    similarity = []
            elif len(review) > 0:
                sql = "SELECT doi, article, similarity FROM review_to_wiki WHERE review='"\
                      + review + "';"
                result = database.execute(sql).fetchall()
                
                if len(result) > 0: # At least one row is returned
                    doi = result[0][0]
                    article = [row[1] for row in result]
                    similarity = [row[2] for row in result]
                else:
                    review = "The review is not found"
                    doi = ""
                    article = []
                    similarity = []
        else:
            review = "Please input a review title or a review doi"
            doi = ""
            article = []
            similarity = []
        
        return render_template("coch_to_wiki2.html", review=review, doi=doi, 
                               article=article, similarity=similarity)
    
@bp.route("/wiki_to_coch", methods=["POST"])
def search_coch():
    if request.method == "POST":
        article = request.form["article"]
        
        if len(article) > 0:
            database = db.get_db()
            
            sql = "SELECT review, doi, similarity FROM wiki_to_review WHERE article='"\
                  + article + "';"
            result = database.execute(sql).fetchall()
            
            if len(result) > 0:
                review = [row[0] for row in result]
                doi = [row[1] for row in result]
                similarity = [row[2] for row in result]
            else:
                article = "The article is not found"
                review = []
                doi = []
                similarity = []
        else:
            review = []
            doi = []
            similarity = []
            article = "Please input a Wikipedia article"
            
        return render_template("wiki_to_coch2.html", article=article, result=zip(review, doi, similarity))
   
