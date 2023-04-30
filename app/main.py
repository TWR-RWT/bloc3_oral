from flask import Flask, render_template, request, jsonify
from app import app, render_template, request, get_db, flash, token_required_auth, redirect, url_for, session, jwt, datetime, timedelta, generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import datetime


@app.route("/produit")###############ok
@token_required_auth
def produit():
    return render_template('/main/product.html')

@app.route('/create_product', methods=['GET', 'POST'])
@token_required_auth
def create_product():
    if request.method == 'POST':
        libelle = request.form['libelle']
        description = request.form['description']
        prix = request.form['prix']
        image = request.files['image']
        categorie = request.form['categorie']

        if image.filename == '':
            uuid_filename = None
        else:
            try:
                #grab image name
                filename = secure_filename(image.filename)
                #set uuid
                uuid_filename = str(uuid.uuid1()) +"_"+ filename
                #save the image
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))

                with get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO mercadona.produits (libelle, description, prix, image, categorie) VALUES (%s, %s, %s, %s, %s)", (libelle, description, prix, uuid_filename, categorie))
                        conn.commit()
                        cur.close()
                flash('Compte créée avec succès')
            except Exception as e:
                print('error: ', e)
                flash('Erreur lors de la création du produit')
        return  redirect(url_for('products'))
    
    return redirect(url_for('index'))








@app.route('/create_product_js', methods=['GET', 'POST'])
@token_required_auth
def create_product_js():
    if request.method == 'POST':
        libelle = request.form['libelle']
        description = request.form['description']
        prix = request.form['prix']
        image = request.files['image']
        categorie = request.form['categorie']

        if image.filename == '':
            uuid_filename = None
        else:
            try:
                #grab image name
                filename = secure_filename(image.filename)
                #set uuid
                uuid_filename = str(uuid.uuid1()) +"_"+ filename
                #save the image
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))

                with get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO mercadona.produits (libelle, description, prix, image, categorie) VALUES (%s, %s, %s, %s, %s)", (libelle, description, prix, uuid_filename, categorie))
                        conn.commit()
                        cur.close()
                return jsonify({'success': True, 'message': 'Produit créé avec succès !'})
            except Exception as e:
                print('error: ', e)
                return jsonify({'success': False, 'message': 'Erreur lors de la création du produit'})
    
    return redirect(url_for('index'))









@app.route('/products')
def products():
    with get_db() as conn:
        with conn.cursor() as cur:
            #cur.execute("SELECT * FROM mercadona.produits")
            cur.execute("""
                SELECT * FROM mercadona.produits 
                LEFT JOIN mercadona.promotions 
                ON produits.id = promotions.product_id AND promotions.start_date <= NOW() AND promotions.end_date >= NOW()
            """)
                        
            products = cur.fetchall()

            # Get all the unique categories
            categories = set([product[5] for product in products])
            conn.commit()
            cur.close()

        img_url = os.path.join(app.config['UPLOAD_FOLDER'], "")
    return render_template('/main/catalogues.html', products=products , img_url=img_url, categories=categories)


@app.route('/promotions', methods=['GET'])
@token_required_auth
def produits_liste_promotions():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, libelle FROM mercadona.produits")
            products = cur.fetchall()
            conn.commit()
            cur.execute("SELECT promotions.id, produits.libelle, promotions.discount, promotions.start_date, promotions.end_date FROM mercadona.promotions LEFT JOIN mercadona.produits ON promotions.product_id = produits.id ORDER BY promotions.start_date DESC")
            rows = cur.fetchall()
            conn.commit()
            cur.close()
    return render_template('/main/discount.html', products=products, promotions=rows)

@app.route('/promotions/submit', methods=['POST'])
@token_required_auth
def submit_promotion():
    #try:
        produits = request.form.getlist('produits')
        print("produits: ")
        print(produits)
        pourcentage = request.form['pourcentage']
        #date_debut = request.form['date_debut']
        #date_fin = request.form['date_fin']

        date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
        date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()


        with get_db() as conn:
            with conn.cursor() as cur:
                for produit_id in produits:
                    cur.execute("SELECT id, start_date, end_date FROM mercadona.promotions WHERE product_id = %s", (produit_id,))
                    rows = cur.fetchall()

                    # Parcourir toutes les promotions existantes pour le produit et remplacer si les périodes se chevauchent
                    for row in rows:
                        promo_id = row[0]
                        promo_start = row[1]
                        promo_end = row[2]

                        if (promo_start <= date_debut <= promo_end) or (promo_start <= date_fin <= promo_end) or (date_debut <= promo_start and date_fin >= promo_end):
                            # Si les périodes se chevauchent, remplacer la promotion existante
                            cur.execute("UPDATE mercadona.promotions SET discount = %s, start_date = %s, end_date = %s WHERE id = %s", (pourcentage, date_debut, date_fin, promo_id))
                        else:
                            # Sinon, insérer une nouvelle promotion
                            cur.execute("INSERT INTO mercadona.promotions (product_id, discount, start_date, end_date) VALUES (%s, %s, %s, %s)", (produit_id, pourcentage, date_debut, date_fin))

                #for produit_id in produits:
                #    cur.execute("INSERT INTO mercadona.promotions (product_id, discount, start_date, end_date) VALUES (%s, %s, %s, %s)",
                #        (produit_id, pourcentage, date_debut, date_fin))
                conn.commit()
                cur.close()
            flash('Promotions créées avec succès')
        return redirect(url_for('index'))
    #except Exception as e:
    #    print('error: ', e)
    #    flash('Erreur lors de la création des promotions')
    #    return redirect(url_for('index'))