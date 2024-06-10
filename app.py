from sympy import symbols, Eq, solve
import streamlit as st
import polars as pl


def calcular_facturacion_agua(consumo_mes):
    """
    Calcula y retorna el volumen de agua consumido en metros cúbicos, el costo total del agua,
    el IGV y verifica si el total calculado coincide con el consumo del mes dado.

    Parámetros:
    - consumo_mes (float): Total del consumo del mes reportado en la factura.

    Retorna:
    - diccionario con los valores de volumen de agua, costo total del agua, IGV calculado, y total verificado.
    """

    costo_m3 = 1.713
    cargo_fijo = 6.26
    mora = 2.03

    y = symbols("y")

    costo_total_agua = costo_m3 * y
    igv = (costo_total_agua + cargo_fijo) * 0.18
    ecuacion = Eq(costo_total_agua + cargo_fijo + igv + mora, consumo_mes)
    volumen_resuelto = solve(ecuacion, y)[0]
    costo_total_agua_resuelto = costo_m3 * volumen_resuelto
    igv_resuelto = (costo_total_agua_resuelto + cargo_fijo) * 0.18
    resultado = {
        "Volumen en m³": round(volumen_resuelto, 5),
        "Costo total del agua (soles)": round(costo_total_agua_resuelto, 2),
        "Cargo fijo": round(cargo_fijo, 2),
        "IGV calculado": round(igv_resuelto, 2),
        "Mora": round(mora, 2),
        "Total verificado": round(
            costo_total_agua_resuelto + cargo_fijo + igv_resuelto + mora, 2
        ),
    }
    return resultado


calcular = st.number_input(
    label="Ingrese el total del consumo del mes según (SEDAPAL): ",
    value=0.0,
    step=0.1,
    format="%.2f",
)

if st.button("Calcular"):
    tabla_valores = pl.DataFrame([calcular_facturacion_agua(consumo_mes=calcular)])
    st.dataframe(tabla_valores.to_pandas(), use_container_width=True, hide_index=True)
    st.success("¡Cálculo realizado con éxito!")
