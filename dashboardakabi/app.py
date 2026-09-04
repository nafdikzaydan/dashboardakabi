import streamlit as st
import plotly.express as px
import pandas as pd
from pyvis.network import Network
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import io
from IPython.core.display import HTML
import sys
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import calendar
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

st_autorefresh(interval=60 * 1000)
# Refresh page every 60 seconds

@st.cache_data(ttl=60)
def get_data(nama_sheet):
    # Tentukan scope untuk mengakses Google Sheets dan Google Drive
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Autentikasi menggunakan secrets dari Streamlit Cloud
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    
    client = gspread.authorize(credentials)

    # Akses Google Spreadsheet
    spreadsheet = client.open("2020 - 2026")
    sheet = spreadsheet.worksheet(nama_sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# df_SL = pd.read_excel('Form Capaian PRSDI.xlsx', sheet_name='SL')
# dfl_SL = get_data()
try:
    df_provitas = get_data("MASTERPROVITAS")

    # Cek hasil
    st.success("Data berhasil dimuat!")
    
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

st.set_page_config(
    page_title="Visualisasi Data Kedelai",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


DATA_CONFIG = {
    "Luas Tanam": {
        "column": "Luas Tanam (Ha)",
        "unit": "Ha",
        "aggregation": "sum"
    },

    "Luas Panen": {
        "column": "Luas Panen (Ha)",
        "unit": "Ha",
        "aggregation": "sum"
    },

    "Produksi": {
        "column": "Produksi (Ton)",
        "unit": "Ton",
        "aggregation": "sum"
    },

    "Produktivitas": {
        "column": "Produktivitas (Ku/Ha)",
        "unit": "Ku/Ha",
        "aggregation": "productivity"
    }
}

MONTH_NAMES = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember"
}


PROVINCE_COORDINATES = {

    # Sumatera
    "11": {
        "Provinsi": "Aceh",
        "Latitude": 4.6951,
        "Longitude": 96.7494
    },
    "12": {
        "Provinsi": "Sumatera Utara",
        "Latitude": 2.1154,
        "Longitude": 99.5451
    },
    "13": {
        "Provinsi": "Sumatera Barat",
        "Latitude": -0.7399,
        "Longitude": 100.8000
    },
    "14": {
        "Provinsi": "Riau",
        "Latitude": 0.2933,
        "Longitude": 101.7068
    },
    "15": {
        "Provinsi": "Jambi",
        "Latitude": -1.4852,
        "Longitude": 102.4381
    },
    "16": {
        "Provinsi": "Sumatera Selatan",
        "Latitude": -3.3194,
        "Longitude": 103.9144
    },
    "17": {
        "Provinsi": "Bengkulu",
        "Latitude": -3.7928,
        "Longitude": 102.2608
    },
    "18": {
        "Provinsi": "Lampung",
        "Latitude": -4.5586,
        "Longitude": 105.4068
    },
    "19": {
        "Provinsi": "Kepulauan Bangka Belitung",
        "Latitude": -2.7411,
        "Longitude": 106.4406
    },
    "21": {
        "Provinsi": "Kepulauan Riau",
        "Latitude": 3.9457,
        "Longitude": 108.1429
    },

    # Jawa
    "31": {
        "Provinsi": "DKI Jakarta",
        "Latitude": -6.2088,
        "Longitude": 106.8456
    },
    "32": {
        "Provinsi": "Jawa Barat",
        "Latitude": -6.8898,
        "Longitude": 107.6405
    },
    "33": {
        "Provinsi": "Jawa Tengah",
        "Latitude": -7.1509,
        "Longitude": 110.1403
    },
    "34": {
        "Provinsi": "DI Yogyakarta",
        "Latitude": -7.7956,
        "Longitude": 110.3695
    },
    "35": {
        "Provinsi": "Jawa Timur",
        "Latitude": -7.5361,
        "Longitude": 112.2384
    },
    "36": {
        "Provinsi": "Banten",
        "Latitude": -6.4058,
        "Longitude": 106.0640
    },

    # Bali & Nusa Tenggara
    "51": {
        "Provinsi": "Bali",
        "Latitude": -8.4095,
        "Longitude": 115.1889
    },
    "52": {
        "Provinsi": "Nusa Tenggara Barat",
        "Latitude": -8.6529,
        "Longitude": 117.3616
    },
    "53": {
        "Provinsi": "Nusa Tenggara Timur",
        "Latitude": -9.6572,
        "Longitude": 124.2587
    },

    # Kalimantan
    "61": {
        "Provinsi": "Kalimantan Barat",
        "Latitude": -0.2788,
        "Longitude": 111.4753
    },
    "62": {
        "Provinsi": "Kalimantan Tengah",
        "Latitude": -1.6815,
        "Longitude": 113.3824
    },
    "63": {
        "Provinsi": "Kalimantan Selatan",
        "Latitude": -3.0926,
        "Longitude": 115.2838
    },
    "64": {
        "Provinsi": "Kalimantan Timur",
        "Latitude": 0.5387,
        "Longitude": 116.4194
    },
    "65": {
        "Provinsi": "Kalimantan Utara",
        "Latitude": 3.0731,
        "Longitude": 116.0414
    },

    # Sulawesi
    "71": {
        "Provinsi": "Sulawesi Utara",
        "Latitude": 0.6247,
        "Longitude": 123.9750
    },
    "72": {
        "Provinsi": "Sulawesi Tengah",
        "Latitude": -1.4300,
        "Longitude": 121.4456
    },
    "73": {
        "Provinsi": "Sulawesi Selatan",
        "Latitude": -3.6688,
        "Longitude": 119.9741
    },
    "74": {
        "Provinsi": "Sulawesi Tenggara",
        "Latitude": -4.1449,
        "Longitude": 122.1746
    },
    "75": {
        "Provinsi": "Gorontalo",
        "Latitude": 0.6999,
        "Longitude": 122.4467
    },
    "76": {
        "Provinsi": "Sulawesi Barat",
        "Latitude": -2.8441,
        "Longitude": 119.2321
    },

    # Maluku
    "81": {
        "Provinsi": "Maluku",
        "Latitude": -3.2385,
        "Longitude": 130.1453
    },
    "82": {
        "Provinsi": "Maluku Utara",
        "Latitude": 1.5709,
        "Longitude": 127.8088
    },

    # Papua
    "91": {
        "Provinsi": "Papua Barat",
        "Latitude": -1.3361,
        "Longitude": 133.1747
    },
    "92": {
        "Provinsi": "Papua Barat Daya",
        "Latitude": -1.3361,
        "Longitude": 130.5060
    },
    "93": {
        "Provinsi": "Papua Selatan",
        "Latitude": -7.7857,
        "Longitude": 139.6818
    },
    "94": {
        "Provinsi": "Papua",
        "Latitude": -4.2699,
        "Longitude": 138.0804
    },
    "95": {
        "Provinsi": "Papua Tengah",
        "Latitude": -3.8792,
        "Longitude": 136.3625
    },
    "96": {
        "Provinsi": "Papua Pegunungan",
        "Latitude": -4.3500,
        "Longitude": 138.7000
    }
}

required_columns = [
    "Tahun",
    "Bulan",
    "Provinsi",
    "Komoditas",
    "Luas Tanam (Ha)",
    "Luas Panen (Ha)",
    "Produksi (Ton)"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df_provitas.columns
]

if missing_columns:

    st.error(
        "Kolom berikut tidak ditemukan: "
        f"{missing_columns}"
    )


def format_number(value, decimals=0):

    if value is None or pd.isna(value):
        return "-"

    if decimals == 0:

        return f"{value:,.0f}"

    return f"{value:,.{decimals}f}"


def get_config(tipe_data):

    return DATA_CONFIG[tipe_data]


def filter_data(
    df,
    tahun=None,
    komoditas=None,
    provinsi=None
):

    result = df.copy()

    if tahun is not None:

        result = result[
            result["Tahun"] == tahun
        ]

    if komoditas is not None:

        result = result[
            result["Komoditas"] == komoditas
        ]

    if provinsi is not None:

        result = result[
            result["Provinsi"] == provinsi
        ]

    return result


def calculate_total(df, tipe_data):

    if df.empty:
        return 0

    config = get_config(tipe_data)

    
    if config["aggregation"] == "sum":

        value = pd.to_numeric(
            df[config["column"]],
            errors="coerce"
        )

        return value.sum()

    
    if config["aggregation"] == "productivity":

        produksi = pd.to_numeric(
            df["Produksi (Ton)"],
            errors="coerce"
        ).fillna(0)

        luas_panen = pd.to_numeric(
            df["Luas Panen (Ha)"],
            errors="coerce"
        ).fillna(0)

        total_produksi = produksi.sum()
        total_luas_panen = luas_panen.sum()

        if total_luas_panen <= 0:
            return 0

        return (
            total_produksi
            / total_luas_panen
            * 10
        )

    return 0


def aggregate_by_province(
    df,
    tipe_data
):

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Provinsi",
                "Value"
            ]
        )

    config = get_config(tipe_data)

    
    if config["aggregation"] == "sum":

        result = (
            df.groupby(
                "Provinsi",
                dropna=True
            )[config["column"]]
            .sum()
            .reset_index()
        )

        result = result.rename(
            columns={
                config["column"]: "Value"
            }
        )

    
    elif config["aggregation"] == "productivity":

        result = (
            df.groupby(
                "Provinsi",
                dropna=True
            )
            .agg({
                "Produksi (Ton)": "sum",
                "Luas Panen (Ha)": "sum"
            })
            .reset_index()
        )

        result["Value"] = 0.0

        mask = (
            result["Luas Panen (Ha)"] > 0
        )

        result.loc[mask, "Value"] = (
            result.loc[mask, "Produksi (Ton)"]
            /
            result.loc[mask, "Luas Panen (Ha)"]
            * 10
        )

    else:

        result = pd.DataFrame(
            columns=[
                "Provinsi",
                "Value"
            ]
        )

    return result


def get_top_province(
    df,
    tipe_data
):

    result = aggregate_by_province(
        df,
        tipe_data
    )

    if result.empty:
        return None, 0

    result = result[
        result["Value"].notna()
    ]

    result = result[
        result["Value"] > 0
    ]

    if result.empty:
        return None, 0

    top = result.loc[
        result["Value"].idxmax()
    ]

    return (
        top["Provinsi"],
        top["Value"]
    )


def count_provinces(df):

    if df.empty:
        return 0

    return (
        df["Provinsi"]
        .dropna()
        .nunique()
    )


def get_top_provinces(
    df,
    tipe_data,
    n=10
):

    result = aggregate_by_province(
        df,
        tipe_data
    )

    result = result[
        result["Value"].notna()
    ]

    result = result[
        result["Value"] > 0
    ]

    result = (
        result
        .sort_values(
            "Value",
            ascending=False
        )
        .head(n)
    )

    return result


def calculate_monthly_trend(
    df,
    tipe_data
):

    months = pd.DataFrame({
        "Bulan": range(1, 13)
    })

    if df.empty:

        months["Value"] = 0
        months["Nama Bulan"] = months["Bulan"].map(
            MONTH_NAMES
        )

        return months

    config = get_config(tipe_data)

    
    if config["aggregation"] == "sum":

        result = (
            df.groupby("Bulan")[
                config["column"]
            ]
            .sum()
            .reset_index()
        )

        result = result.rename(
            columns={
                config["column"]: "Value"
            }
        )

    
    elif config["aggregation"] == "productivity":

        result = (
            df.groupby("Bulan")
            .agg({
                "Produksi (Ton)": "sum",
                "Luas Panen (Ha)": "sum"
            })
            .reset_index()
        )

        result["Value"] = 0.0

        mask = (
            result["Luas Panen (Ha)"] > 0
        )

        result.loc[mask, "Value"] = (
            result.loc[mask, "Produksi (Ton)"]
            /
            result.loc[mask, "Luas Panen (Ha)"]
            * 10
        )

        result = result[
            ["Bulan", "Value"]
        ]

    else:

        result = pd.DataFrame(
            columns=[
                "Bulan",
                "Value"
            ]
        )

    
    result = months.merge(
        result,
        on="Bulan",
        how="left"
    )

    result["Value"] = (
        result["Value"]
        .fillna(0)
    )

    result["Nama Bulan"] = (
        result["Bulan"]
        .map(MONTH_NAMES)
    )

    return result


def calculate_year_comparison(
    df,
    tahun,
    komoditas,
    tipe_data
):

    current_df = filter_data(
        df,
        tahun=tahun,
        komoditas=komoditas
    )

    previous_df = filter_data(
        df,
        tahun=tahun - 1,
        komoditas=komoditas
    )

    current_value = calculate_total(
        current_df,
        tipe_data
    )

    previous_value = calculate_total(
        previous_df,
        tipe_data
    )

    difference = (
        current_value
        - previous_value
    )

    if previous_value != 0:

        percentage = (
            difference
            / previous_value
            * 100
        )

    else:

        percentage = None

    return {
        "current_year": tahun,
        "previous_year": tahun - 1,
        "current_value": current_value,
        "previous_value": previous_value,
        "difference": difference,
        "percentage": percentage
    }


def calculate_yearly_monthly_comparison(
    df,
    tahun,
    komoditas,
    tipe_data
):

    current_df = filter_data(
        df,
        tahun=tahun,
        komoditas=komoditas
    )

    previous_df = filter_data(
        df,
        tahun=tahun - 1,
        komoditas=komoditas
    )

    current_trend = calculate_monthly_trend(
        current_df,
        tipe_data
    )

    previous_trend = calculate_monthly_trend(
        previous_df,
        tipe_data
    )

    current_trend["Tahun"] = tahun

    previous_trend["Tahun"] = (
        tahun - 1
    )

    result = pd.concat(
        [
            current_trend,
            previous_trend
        ],
        ignore_index=True
    )

    return result


def prepare_map_data(
    df,
    tipe_data
):

    province_data = aggregate_by_province(
        df,
        tipe_data
    )

    if province_data.empty:
        return province_data

    province_data["Kode Wilayah"] = (
        df.groupby("Provinsi")["Kode Wilayah"]
        .first()
        .reindex(
            province_data["Provinsi"]
        )
        .values
    )

    province_data["Kode Wilayah"] = (
        province_data["Kode Wilayah"]
        .astype("string")
        .str.strip()
    )

    coordinates = pd.DataFrame(
        [
            {
                "Kode Wilayah": code,
                **data
            }
            for code, data
            in PROVINCE_COORDINATES.items()
        ]
    )

    result = province_data.merge(
        coordinates,
        on="Kode Wilayah",
        how="left"
    )

    return result


def create_sidebar():

    with st.sidebar:

        st.title("🌾 Visualisasi Data Kedelai")

        st.divider()

        
        tahun_list = sorted(
            df_provitas["Tahun"]
            .dropna()
            .unique(),
            reverse=True
        )

        if not tahun_list:

            st.error(
                "Tidak ada data tahun."
            )

            st.stop()

        selected_tahun = st.selectbox(
            "Pilih Tahun",
            tahun_list
        )

        
        komoditas_list = sorted(
            df_provitas["Komoditas"]
            .dropna()
            .unique()
        )

        selected_komoditas = st.selectbox(
            "Pilih Komoditas",
            komoditas_list
        )

        
        selected_tipe_data = st.selectbox(
            "Pilih Tipe Data",
            list(DATA_CONFIG.keys())
        )

        st.divider()

        st.caption(
            "Gunakan filter di atas untuk "
            "mengubah seluruh visualisasi."
        )

    return (
        selected_tahun,
        selected_komoditas,
        selected_tipe_data
    )


def render_kpis(
    df_filtered,
    tipe_data
):

    total = calculate_total(
        df_filtered,
        tipe_data
    )

    top_province, top_value = (
        get_top_province(
            df_filtered,
            tipe_data
        )
    )

    province_count = count_provinces(
        df_filtered
    )

    config = get_config(
        tipe_data
    )

    unit = config["unit"]

    col1, col2, col3 = st.columns(3)

    
    with col1:

        st.metric(
            label=f"Total {tipe_data}",
            value=(
                f"{format_number(total, 2)} "
                f"{unit}"
            )
        )

    
    with col2:

        st.metric(
            label="Provinsi Teratas",
            value=(
                top_province
                if top_province
                else "-"
            )
        )

        if top_province:

            st.caption(
                f"{format_number(top_value, 2)} "
                f"{unit}"
            )

    
    with col3:

        st.metric(
            label="Provinsi Dengan Data",
            value=(
                f"{province_count} Provinsi"
            )
        )


def render_monthly_trend(
    df_filtered,
    tipe_data
):

    trend = calculate_monthly_trend(
        df_filtered,
        tipe_data
    )

    config = get_config(
        tipe_data
    )

    fig = px.line(
        trend,
        x="Nama Bulan",
        y="Value",
        markers=True,
        title=(
            f"Tren Bulanan "
            f"{tipe_data}"
        ),
        labels={
            "Nama Bulan": "Bulan",
            "Value": (
                f"{tipe_data} "
                f"({config['unit']})"
            )
        }
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            categoryorder="array",
            categoryarray=[
                MONTH_NAMES[i]
                for i in range(1, 13)
            ]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_top_10(
    df_filtered,
    tipe_data
):

    result = get_top_provinces(
        df_filtered,
        tipe_data,
        n=10
    )

    if result.empty:

        st.info(
            "Tidak ada data provinsi."
        )

        return

    config = get_config(
        tipe_data
    )

    chart_data = result.sort_values(
        "Value",
        ascending=True
    )

    fig = px.bar(
        chart_data,
        x="Value",
        y="Provinsi",
        orientation="h",
        text="Value",
        title="Top 10 Provinsi",
        labels={
            "Value": (
                f"{tipe_data} "
                f"({config['unit']})"
            ),
            "Provinsi": ""
        }
    )

    fig.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside"
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_distribution(
    df_filtered,
    tipe_data
):

    result = aggregate_by_province(
        df_filtered,
        tipe_data
    )

    result = result[
        result["Value"] > 0
    ]

    if result.empty:

        st.info(
            "Tidak ada data distribusi."
        )

        return

    
    result = result.sort_values(
        "Value",
        ascending=False
    )

    top_10 = result.head(10).copy()

    other_value = (
        result.iloc[10:]["Value"].sum()
    )

    if other_value > 0:

        other = pd.DataFrame({
            "Provinsi": ["Lainnya"],
            "Value": [other_value]
        })

        chart_data = pd.concat(
            [
                top_10,
                other
            ],
            ignore_index=True
        )

    else:

        chart_data = top_10

    fig = px.pie(
        chart_data,
        names="Provinsi",
        values="Value",
        hole=0.4,
        title="Distribusi Provinsi"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_year_comparison_chart(
    df_provitas,
    tahun,
    komoditas,
    tipe_data
):

    comparison = calculate_yearly_monthly_comparison(
        df_provitas,
        tahun,
        komoditas,
        tipe_data
    )

    config = get_config(
        tipe_data
    )

    previous_df = filter_data(
        df_provitas,
        tahun=tahun - 1,
        komoditas=komoditas
    )

    if previous_df.empty:

        st.info(
            f"Data tahun {tahun - 1} "
            "tidak tersedia."
        )

    fig = px.line(
        comparison,
        x="Nama Bulan",
        y="Value",
        color="Tahun",
        markers=True,
        title=(
            f"Perbandingan Tren "
            f"{tipe_data} "
            f"{tahun} vs {tahun - 1}"
        ),
        labels={
            "Nama Bulan": "Bulan",
            "Value": (
                f"{tipe_data} "
                f"({config['unit']})"
            ),
            "Tahun": "Tahun"
        }
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            categoryorder="array",
            categoryarray=[
                MONTH_NAMES[i]
                for i in range(1, 13)
            ]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_percentage_comparison(
    df_provitas,
    tahun,
    komoditas,
    tipe_data
):

    comparison = calculate_year_comparison(
        df_provitas,
        tahun,
        komoditas,
        tipe_data
    )

    percentage = comparison[
        "percentage"
    ]

    difference = comparison[
        "difference"
    ]

    current_value = comparison[
        "current_value"
    ]

    previous_value = comparison[
        "previous_value"
    ]

    config = get_config(
        tipe_data
    )

    st.subheader(
        "Perbandingan Persentase"
    )

    if previous_value == 0:

        st.metric(
            label=(
                f"{tipe_data} vs "
                f"{tahun - 1}"
            ),
            value="N/A"
        )

        st.caption(
            f"Data tahun {tahun - 1} "
            "tidak tersedia atau bernilai 0."
        )

        return

    st.metric(
        label=(
            f"Perubahan {tipe_data}"
        ),
        value=(
            f"{percentage:+.2f}%"
        ),
        delta=(
            f"{difference:+,.2f} "
            f"{config['unit']}"
        )
    )

    st.caption(
        f"{tahun}: "
        f"{format_number(current_value, 2)} "
        f"{config['unit']}  |  "
        f"{tahun - 1}: "
        f"{format_number(previous_value, 2)} "
        f"{config['unit']}"
    )


def render_map(
    df_filtered,
    tipe_data
):

    map_data = prepare_map_data(
        df_filtered,
        tipe_data
    )

    if map_data.empty:

        st.info(
            "Tidak ada data untuk peta."
        )

        return

    map_data = map_data[
        map_data["Latitude"].notna()
        &
        map_data["Longitude"].notna()
    ]

    if map_data.empty:

        st.warning(
            "Koordinat provinsi tidak "
            "ditemukan."
        )

        return

    config = get_config(
        tipe_data
    )

    fig = px.scatter_geo(
        map_data,
        lat="Latitude",
        lon="Longitude",
        size="Value",
        color="Value",
        hover_name="Provinsi",
        hover_data={
            "Kode Wilayah": True,
            "Value": ":,.2f",
            "Latitude": False,
            "Longitude": False
        },
        title=(
            f"Peta Sebaran Geografis "
            f"{tipe_data}"
        ),
        projection="mercator",
        scope="asia",
        color_continuous_scale="YlGn"
    )

    fig.update_geos(
        center={
            "lat": -2,
            "lon": 118
        },
        projection_scale=4.5,
        showland=True,
        landcolor="#F4F4F4",
        showcountries=True,
        countrycolor="#999999"
    )

    fig.update_layout(
        height=600,
        coloraxis_colorbar={
            "title": config["unit"]
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def main():


    (
        selected_tahun,
        selected_komoditas,
        selected_tipe_data
    ) = create_sidebar()


    st.title(
        "🌾 Visualisasi Data Kedelai"
    )

    st.caption(
        f"Tahun {selected_tahun} • "
        f"{selected_komoditas} • "
        f"{selected_tipe_data}"
    )


    df_filtered = filter_data(
        df_provitas,
        tahun=selected_tahun,
        komoditas=selected_komoditas
    )


    render_kpis(
        df_filtered,
        selected_tipe_data
    )
    
    st.divider()


    st.subheader(
        "Tren Bulanan"
    )

    render_monthly_trend(
        df_filtered,
        selected_tipe_data
    )


    col1, col2 = st.columns(2)

    with col1:

        render_top_10(
            df_filtered,
            selected_tipe_data
        )

    with col2:

        render_distribution(
            df_filtered,
            selected_tipe_data
        )


    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        render_year_comparison_chart(
            df_provitas,
            selected_tahun,
            selected_komoditas,
            selected_tipe_data
        )

    with col2:

        render_percentage_comparison(
            df_provitas,
            selected_tahun,
            selected_komoditas,
            selected_tipe_data
        )


    st.divider()

    st.subheader(
        "Peta Sebaran Geografis"
    )

    render_map(
        df_filtered,
        selected_tipe_data
    )


    with st.expander(
        "Lihat Data Terfilter"
    ):

        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()