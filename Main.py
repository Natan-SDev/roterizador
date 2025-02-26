import streamlit as st
import webbrowser

st.title('Roterizador')

    # Exibindo o resumo do aplicativo
st.subheader("Resumo do App")
st.write("""
    Este aplicativo permite calcular a **melhor rota** entre um ponto de **origem** e até **9 pontos de destino**.
    O app encontra a rota mais curta que passa por todos os pontos de forma eficiente.
    Além disso, gera links para a rota no **Google Maps** para fácil visualização e navegação.

    ### Funcionalidades principais:
    1. **Entrada de Endereços:** Você pode inserir o ponto de **origem** e até **9 pontos de destino**.
    2. **Cálculo da Melhor Rota:** O algoritmo encontra a melhor rota, considerando as distâncias geográficas entre os pontos e também a questão do ultimo ponto em relação a origem.
    3. **Links do Google Maps:** O app gera links interativos para visualizar a rota no **Google Maps**.
    4. **Cálculo das Distâncias:** As distâncias são calculadas usando as coordenadas geográficas obtidas pelo **Geopy**.

    ### Tecnologias utilizadas:
    - **Streamlit** para a interface interativa.
    - **Geopy** para geolocalização e cálculo das distâncias.
    - **NetworkX** para manipulação de grafos e solução do Problema do Caixeiro Viajante.
    """)



st.sidebar.link_button('Visite meu LinkedIn', 'www.linkedin.com/in/natanael-silva-50b8b2289')

st.markdown("<br><br>", unsafe_allow_html=True)
# Botão para ir ao LinkedIn
if st.button('Visite meu LinkedIn'):
    webbrowser.open('www.linkedin.com/in/natanael-silva-50b8b2289')  


  
