#Testiranje u Postman
#   
#   
#   GET (prikaz jednog ili svih zadataka)
#       -> port adresa/zadaci
#       -> port adresa/zadaci/id trazenog zadatka
#   
#   POST (dodavanje novog zadatka)
#       -> port adresa; raw body: {"param1":"vrednost","param2":"vrednost", itd.}
#  
#   PUT (azuriranje zadatka novim vrednostima)
#       -> port adresa/zadaci/id zadatka za azuriranje; raw body: {"param1":"vrednost"}
#   
#   DELETE (brisanje zadatka)
#       -> port adresa/zadaci/id zadatka za brisanje
# #



from flask import Blueprint, jsonify, request
from models import db, Zadatak
from datetime import datetime


routes = Blueprint('routes', __name__) 



@routes.route('/')
def index():
    return jsonify({'msg':'Spisak zadataka (id, naziv, opis, uradjeno, datum)'})

@routes.route('/zadaci',methods=['GET'])
def svi_zadaci():
    query_params = request.args
    filter_done = query_params.get('uradjeno',None)
    sort_by = query_params.get('sort by', 'id')

    query = Zadatak.query

    if filter_done is not None:
         query = query.filter_by(done=filter_done.lower()=='true')

    zadaci = query.order_by(getattr(Zadatak,sort_by)).all()
    return jsonify([{
        'id':zad.id,
        'naziv': zad.naziv,
        'opis':zad.opis,
        'uradjeno':zad.uradjeno,
        'datum':zad.datum.isoformat() if zad.datum else None
    } for zad in zadaci]), 200



@routes.route('/zadaci/<int:zad_id>', methods = ['GET'])
def zadatak(zad_id):
    zadatak = Zadatak.query.filter_by(id=zad_id).first()
    if zadatak is None:
        return jsonify({'msg':'Zadatak nije pronadjen'}), 404
    return jsonify({
        'id':zadatak.id,
        'naziv':zadatak.naziv,
        'opis':zadatak.opis,
        'uradjeno':zadatak.uradjeno,
        'datum':zadatak.datum.isoformat() if zadatak.datum else None
    }), 200


@routes.route('/zadaci',methods = ['POST'])
def dodaj_zadatak():
    data = request.get_json()
    naziv = data['naziv']
    opis = data.get('opis','')
    datum_str = data.get('datum','')

    if datum_str:
        try:
            datum = datetime.fromisoformat(datum_str)
        except ValueError:
            return jsonify({'msg':'Pogresan format datuma'})
    
    novi_zadatak = Zadatak(naziv=naziv, opis=opis) #mozda dodati datum=datum trenutno nepotrebno, za novi zadatak u pocetku dovoljan samo naziv
    db.session.add(novi_zadatak)
    db.session.commit()

    return jsonify({'msg':'Zadatak dodat'}), 201



@routes.route('/zadaci/<int:zad_id>',methods=['PUT'])
def azuriraj_zadatak(zad_id):
    data = request.get_json()
    naziv = data.get('naziv')
    opis = data.get('opis')
    uradjeno = data.get('uradjeno')
    datum_str = data.get('datum','')

    zadatak = Zadatak.query.filter_by(id=zad_id).first()
    if zadatak is None:
        return jsonify({'msg':'Zadatak nije pronadjen'}),404
    
    if naziv is not None:
        zadatak.naziv = naziv
    if opis is not None:
        zadatak.opis = opis
    if uradjeno is not None:
        zadatak.uradjeno = uradjeno
    if datum_str is not None:
        try:
            zadatak.datum = datetime.fromisoformat(datum_str)
        except ValueError:
            return jsonify({'msg','Pogresan format datuma'}), 400
        
    db.session.commit()
    
    return jsonify({'msg':'Zadatak azuriran'}), 200




@routes.route('/zadaci/<int:zad_id>',methods = ['DELETE'])
def obrisi_zadatak(zad_id):

    zadatak = Zadatak.query.filter_by(id=zad_id).first()
    
    if zadatak is None:
        return jsonify({'msg':'Zadatak nije pronadjen'})
    
    db.session.delete(zadatak)
    db.session.commit()

    return jsonify({'msg':'Zadatak obrisan'}), 200




