from flask import Flask, render_template, jsonify
import psycopg2
import numpy as np
from scipy import signal
import datetime

app = Flask(__name__)

def load_data():
    hostname = 'localhost'
    database = 'Hydrolog'
    username = 'postgres'
    password = 'DB_PASS'
    port_id = 5432
    
    try:
        connection = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port_id
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "Hydrolog1"."hydro_sensor2" LIMIT 1000;')
        rows = cursor.fetchall()
        print("Fetched rows:", rows)  # Debug print
        return rows
    except Exception as error:
        print("Error connecting to the database or executing the query:", error)
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def seconds_to_datetime_str(seconds):
    base_time = datetime.datetime(2000, 1, 1)
    time = base_time + datetime.timedelta(seconds=seconds)
    return time.strftime('%d.%m %H:%M')

def apply_fir_filter(y_values, time_values):
    time_intervals = np.diff(time_values)
    average_time_interval = np.mean(time_intervals)
    sampling_rate = 1 / average_time_interval
    nyquist_rate = sampling_rate / 2
    cutoff_fraction = 1 / 20
    cutoff_frequency = cutoff_fraction * nyquist_rate
    num_taps = 101
    fir_coeff = signal.firwin(num_taps, cutoff_frequency, fs=sampling_rate)
    y_smooth = signal.lfilter(fir_coeff, 1.0, y_values)
    return y_smooth

def apply_kalman_filter(values):
    n = len(values)
    x_est = np.zeros(n)
    P = np.zeros(n)
    Q = 1e-5  # Process variance
    R = 0.1 ** 2  # Measurement variance

    x_est[0] = values[0]  # Initial estimate
    P[0] = 1.0  # Initial estimate error

    for k in range(1, n):
        # Prediction step
        x_pred = x_est[k-1]
        P_pred = P[k-1] + Q

        # Update step
        K = P_pred / (P_pred + R)
        x_est[k] = x_pred + K * (values[k] - x_pred)
        P[k] = (1 - K) * P_pred

    return x_est


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
@app.route('/data')
def data():
    rows = load_data()
    if not rows:
        return jsonify({"error": "No data found"}), 500

    x_values = [seconds_to_datetime_str(row[0]) for row in rows]
    y_values = [row[1] for row in rows]  # pH Value
    ec_values = [row[2] for row in rows]
    water_temp = [row[3] if row[3] is not None else 'N/A' for row in rows]
    air_temp = [row[4] if row[4] is not None else 'N/A' for row in rows]
    humidity = [row[5] if row[5] is not None else 'N/A' for row in rows]
    time_values = [row[0] for row in rows]

    y_smooth = apply_fir_filter(y_values, time_values)
    y_kalman = apply_kalman_filter(y_values)

    return jsonify({
        'x_values': x_values,
        'y_values': y_values,
        'ec_values': ec_values,
        'water_temp': water_temp,
        'air_temp': air_temp,
        'humidity': humidity,
        'y_smooth': y_smooth.tolist(),
        'y_kalman': y_kalman.tolist()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
