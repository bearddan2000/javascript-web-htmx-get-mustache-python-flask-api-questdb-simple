import logging, requests
import urllib.parse as par

logging.basicConfig(level=logging.INFO)

class Endpoints():

    def __init__(self) -> None:
        self.client = QuestClient()

    def get_all(self):
        sql = "select dog_id, breed, color from dog"
        return self.client.return_results(sql)
    
    def get_by_breed(self, dog_breed):
        try:
            sql = f"select dog_id, breed, color from dog where breed = '{dog_breed}'"
            return self.client.return_results(sql)
        except:
            return self.get_all()
    
    def get_by_color(self, dog_color):
        try:
            sql = f"SELECT dog_id, breed, color FROM dog WHERE color = '{dog_color}'"
            return self.client.return_results(sql)
        except:
            return self.get_all()
        
    def insert(self, dog_breed, dog_color):
        try:
            records = [
                { "breed": dog_breed,"color": dog_color,"id": 99}
            ]
            self.client.insert_record(records)
        except:
            logging.warning("insert failed: breed => " + dog_breed + ", color => " + dog_color)
            pass
        return self.get_all()


class QuestClient():

    SERVICE_URL = "http://db:9000/exec?query="
    
    def __new__(cls):
        """use singleton design pattern for a single instance"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(QuestClient, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        query = "select * from dog"
        r = requests.get(self.SERVICE_URL + query)
        if r.status_code == 400:
            records = [
                { "breed": "Am Bulldog","color": "White","id": 1},
                { "breed": "Blue Tick","color": "Grey","id": 2},
                { "breed": "Labrador","color": "Black", "id": 3},
                { "breed": "Gr Shepard", "color": "Brown", "id": 4}
            ]
            self.create_table()
            self.insert_record(records)

    def create_table(self):
        query = 'create table dog'\
            '(dog_id int,'\
            'breed String,'\
            'color String,'\
            'timestamp timestamp)'\
            'timestamp(timestamp)'
        r = requests.get(self.SERVICE_URL + query)
        logging.info(r.status_code)

    def insert_record(self, records):
        
        for record in records:
            id = record['id']
            breed = record['breed']
            color = record['color']

            query = "insert into dog (dog_id, breed, color, timestamp) values("\
                + str(id) + ",'"\
                + str(breed) + "','" \
                + str(color) +"',systimestamp())"
            r = requests.get(self.SERVICE_URL + query)
        
    def return_results(self, sql):
        try:
            query = par.quote(sql)
            r = requests.get(self.SERVICE_URL + query)
            x = r.json()
            results = [
            {
                "id": o[0],
                "name": o[1],
                "color": o[2]
            } for o in x['dataset']]
            return {'data': results, 'count': x['count']}
        except:
            return sql

