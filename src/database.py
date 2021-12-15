import psycopg2 as pg
import datetime as dt
conn = pg.connect(database='RTCS_WEATHER', user='postgres',
                  host='localhost', password='adminka')
cur = conn.cursor()


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_last_data(date):
    date_start = date-dt.timedelta(days=4)
    date_end = date.strftime("%Y-%m-%d")
    sql = "SELECT * FROM \"DAILY_METRICS\" WHERE date >= %s AND date < %s;"
    cur.execute(sql, (date_start, date_end))
    return _dictfetchall(cur)


def insert_current(data):
    sql = "UPDATE \"DAILY_METRICS\" SET (\"date\", \"mintempC\", \"maxtempC\", \"avgtempC\", \"humidity\", \"sunHour\", \"DewPointC\") = \
            ('{date}', {mintempC}, {maxtempC}, {avgtempC}, {humidity}, {sunHour}, {DewPointC}) WHERE date='{date}'; \
            INSERT INTO \"DAILY_METRICS\" \
            SELECT '{date}', {mintempC}, {maxtempC}, {avgtempC}, {humidity}, {sunHour}, {DewPointC} \
            WHERE NOT EXISTS (SELECT 1 FROM \"DAILY_METRICS\" WHERE date='{date}');".format(**data)
    cur.execute(sql)
    conn.commit()
