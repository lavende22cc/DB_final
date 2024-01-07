"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect(
    user = "postgres",
    password = "Siyu0630",
    host = "database-r.cagfr8vhddlj.us-east-1.rds.amazonaws.com",
    port = "5432",
    database = "final1"
)

con = connection.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        destination = request.form['destination']
        flightPrice = request.form['flightPrice']
        hotelPrice = request.form['hotelPrice']
        season = request.form['season']
        sort = request.form['sort']

        #hotel
        if(hotelPrice == '1'):
            query_hotel = '''select hotel_name, fixed_price / 2, recommendation from hotel where jr_station = \'''' + destination + "\'" + ''' and fixed_price / 2 < 1000 order by recommendation desc limit 5'''
        if(hotelPrice == '2'):
            query_hotel = '''select hotel_name, fixed_price / 2, recommendation from hotel where jr_station = \'''' + destination + "\'" + ''' and fixed_price / 2 <= 3000 and fixed_price / 2 > 1000 order by recommendation desc limit 5'''
        if(hotelPrice == '3'):
            query_hotel = '''select hotel_name, fixed_price / 2, recommendation from hotel where jr_station = \'''' + destination + "\'" + ''' and fixed_price / 2 > 3000 order by recommendation desc limit 5'''
        
        #JR
        query_for_JR_station = '''select a.full_name, iata, jr_station_name, ticket_price_jpy as jr_$, duration as avg_jr_time from airport_to_jr aj join airport a on aj.airport_iata = a.iata where jr_station_name = \'''' + destination + "\'"

        #flight        
        if(flightPrice == '1' and season == '1'):
            query_flight_price = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t1_pri as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price <= 10000
), wealthy_1_pri as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t1_pri w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time
	order by avg(ticket_price) asc
	limit 5
)
select * from wealthy_1_pri'''
            query_flight_time = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t1_dur as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = jr_station = \'''' + destination + "\'" + '''  
	and ticket_price <= 10000
), wealthy_1_dur as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t1_dur w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc
	limit 5
)
select * from wealthy_1_dur'''
            query_flight_mix = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t1_all as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price <= 10000
), wealthy_1_all as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t1_all w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from wealthy_1_all'''
        if(flightPrice == '2' and season == '1'):
            query_flight_price = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t2_pri as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price between 15000 and 30000
), wealthy_2_pri as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t2_pri w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time
	order by avg(ticket_price) asc
	limit 5
)
select * from wealthy_2_pri'''
            query_flight_time = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t2_dur as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price between 15000 and 30000
), wealthy_2_dur as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t2_dur w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc
	limit 5
)
select * from wealthy_2_dur'''
            query_flight_mix = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t2_all as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price between 15000 and 30000
), wealthy_2_all as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t2_all w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from wealthy_2_all'''
        if(flightPrice == '3' and season == '1'):
            query_flight_price = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t3_pri as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price >= 20000
), wealthy_3_pri as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t3_pri w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time
	order by avg(ticket_price) desc
	limit 5
)
select * from wealthy_3_pri'''
            query_flight_time = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t3_dur as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price >= 30000
), wealthy_3_dur as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t3_dur w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc
	limit 5
)
select * from wealthy_3_dur'''
            query_flight_mix = '''with wealthy_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) desc
	limit 30
), wealthy_t_ as (
	select w.iata, w.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from wealthy_date w, airport_to_flight f
	where w.date = f.date and w.iata = f.landing_airport_iata
), wealthy_t3_all as (
	select *
	from wealthy_t_ w
	join airport_to_jr aj on w.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + ''' 
	and ticket_price >= 25000
), wealthy_3_all as (
	select full_name, full_name_mandarin, w.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from wealthy_t3_all w
	join airport a on w.iata = a.iata
	group by full_name, full_name_mandarin, w.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from wealthy_3_all'''
        if(flightPrice == '1' and season == '0'):
            query_flight_price = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t1_pri as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price <= 10000
), poor_1_pri as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from poor_t1_pri p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time
	order by avg(ticket_price)
	limit 5
)
select * from poor_1_pri'''
            query_flight_time = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t1_dur as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price <= 10000
	order by fly_duration
), poor_1_dur as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t1_dur p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration
	limit 5
)
select * from poor_1_dur'''
            query_flight_mix = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t1_all as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price <= 10000
	order by fly_duration asc
), poor_1_all as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t1_all p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from poor_1_all'''
        if(flightPrice == '2' and season == '0'):
            query_flight_price = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t2_pri as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price between 7500 and 30000
), poor_2_pri as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from poor_t2_pri p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time
	order by avg(ticket_price)
	limit 5
)
select * from poor_2_pri'''
            query_flight_time = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t2_dur as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price <= 30000
	order by fly_duration
), poor_2_dur as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t2_dur p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration
	limit 5
)
select * from poor_2_dur'''
            query_flight_mix = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t2_all as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price between 7500 and 30000
	order by fly_duration asc
), poor_2_all as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t2_all p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from poor_2_all;'''
        if(flightPrice == '3' and season == '0'):
            query_flight_price = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t3_pri as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price >= 10000
), poor_3_pri as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, avg(fly_duration) as avg_duration, avg(ticket_price) as avg_ticket_$
	from poor_t3_pri p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time
	order by avg(ticket_price) asc
	limit 5
)
select * from poor_3_pri'''
            query_flight_time = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t3_dur as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	order by fly_duration
), poor_3_dur as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t3_dur p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration
	limit 5
)
select * from poor_3_dur'''
            query_flight_mix = '''with poor_date as (
	select landing_airport_iata as iata, date, avg(ticket_price) as avg_fly_$
	from airport_to_flight
	group by landing_airport_iata, date
	order by avg(ticket_price) asc
	limit 30
), poor_t_ as (
	select p.iata, p.date, ticket_price, departure_time, landing_time, duration as fly_duration, airline
	from poor_date p, airport_to_flight f
	where p.date = f.date and p.iata = f.landing_airport_iata
), poor_t3_all as (
	select *
	from poor_t_ p
	join airport_to_jr aj on p.iata = aj.airport_iata
	where aj.jr_station_name = \'''' + destination + "\'" + '''
	and ticket_price >= 10000
	order by fly_duration asc
), poor_3_all as (
	select full_name, full_name_mandarin, p.iata, airline,
	departure_time, landing_time, fly_duration, avg(ticket_price) as avg_ticket_$
	from poor_t3_all p
	join airport a on p.iata = a.iata
	group by full_name, full_name_mandarin, p.iata, airline, departure_time, landing_time, fly_duration
	order by fly_duration asc, avg_ticket_$ asc
	limit 5
)
select * from poor_3_all'''

        # if(sort == '1'):
        #     con.execute(query_flight_price)
        #     table_data_flight = con.fetchall()
        #     return render_template('result.html', table_data_jr=table_data_jr, table_data_flight=table_data_flight, table_data_hotel=table_data_hotel)
        # if(sort == '2'):
        #     con.execute(query_flight_time)
        #     table_data_flight = con.fetchall()
        #     return render_template('result.html', table_data_jr=table_data_jr, table_data_flight=table_data_flight, table_data_hotel=table_data_hotel)
        # if(sort == '3'):            
        #     con.execute(query_flight_mix)
        #     table_data_flight = con.fetchall()
        #     return render_template('result.html', table_data_jr=table_data_jr, table_data_flight=table_data_flight, table_data_hotel=table_data_hotel)

        con.execute(query_hotel)
        table_data_hotel = con.fetchall()
        con.execute(query_for_JR_station)
        table_data_jr = con.fetchall()

        con.execute(query_flight_price)
        table_flight_price = con.fetchall()
        con.execute(query_flight_time)
        table_flight_time = con.fetchall()
        con.execute(query_flight_mix)
        table_flight_mix = con.fetchall()

        return render_template('result.html', result_table_jr=table_data_jr, result_table_hotel=table_data_hotel, result_table_flight_price=table_flight_price, result_table_flight_time=table_flight_time, result_table_flight_mix=table_flight_mix)
    return render_template('mainPage.html')

if __name__ == '__main__':
    app.run()


#return a page
    
