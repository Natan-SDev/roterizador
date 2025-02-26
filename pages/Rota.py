import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import networkx as nx
import itertools
import urllib.parse

# Função para buscar as coordenadas geográficas usando o Geopy
def get_coordinates(address):
    geolocator = Nominatim(user_agent="distance_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Função para calcular a distância entre dois pontos
def calculate_distance(point1, point2):
    return geodesic(point1, point2).km

# Função para resolver o Problema do Caixeiro Viajante (TSP) e encontrar a melhor rota
def solve_tsp(distances, start_point):
    points = list(distances.keys())
    points.remove(start_point)  # Remove o ponto de origem das permutações
    shortest_path = None
    min_distance = float('inf')

    # Gerando todas as permutações possíveis dos pontos restantes para encontrar a menor rota
    for perm in itertools.permutations(points):
        current_path = [start_point] + list(perm)
        total_distance = 0

        # Calcula a distância total para essa permutação
        for i in range(len(current_path) - 1):
            total_distance += distances[current_path[i]][current_path[i + 1]]
        
        # Ajuste no cálculo da distância do último ponto para o primeiro ponto
        total_distance += distances[current_path[-1]][current_path[0]]  # Considera o retorno ao ponto inicial

        # Atualizando a melhor rota
        if total_distance < min_distance:
            min_distance = total_distance
            shortest_path = current_path

    return shortest_path, min_distance

# Função para gerar o link do Google Maps com a rota
def generate_google_maps_link(route):
    # Cria o link do Google Maps com a rota
    base_url = "https://www.google.com/maps/dir/"
    route_str = "/".join(route)
    return f"{base_url}{urllib.parse.quote(route_str)}"

# Função principal para criar o grafo e calcular as distâncias
def calculate_route():
    st.title('Calculadora de Distâncias e Melhor Rota')

    # Input do ponto de origem
    start_address = st.text_input("Ponto de Origem", "UPA Imbiribeira")

    # Limitar a 10 pontos (inclusive o ponto de origem)
    max_points = 10

    other_addresses = []
    for i in range(max_points - 1):  # O ponto de origem já foi capturado
        address = st.text_input(f"Ponto de Destino {i+1}", "")
        if address:
            other_addresses.append(address)

    # Verificar se o número de pontos ultrapassou o limite
    if len(other_addresses) > max_points - 1:
        st.warning(f"Você pode adicionar no máximo {max_points - 1} pontos de destino.")
        return

    # Se não houver nenhum ponto de origem ou outros pontos, alerta o usuário
    if not start_address or not other_addresses:
        st.warning("Por favor, preencha o ponto de origem e ao menos um outro ponto.")
        return

    addresses = [start_address] + other_addresses

    # Quando o botão de calcular for pressionado, executa a lógica
    if st.button('Calcular Melhor Rota'):
        # Buscar coordenadas para cada endereço
        coordinates = []
        for address in addresses:
            coords = get_coordinates(address)
            if coords:
                coordinates.append(coords)
            else:
                st.warning(f"Não foi possível encontrar o endereço: {address}")
                return

        # Criando o grafo
        G = nx.Graph()

        # Adicionar nós no grafo (endereço como nó)
        for i, address in enumerate(addresses):
            G.add_node(address, pos=coordinates[i])

        # Calcular as distâncias e adicionar as arestas com os pesos
        distances = {}
        for i in range(len(addresses)):
            for j in range(i + 1, len(addresses)):
                dist = calculate_distance(coordinates[i], coordinates[j])
                G.add_edge(addresses[i], addresses[j], weight=dist)
                if addresses[i] not in distances:
                    distances[addresses[i]] = {}
                if addresses[j] not in distances:
                    distances[addresses[j]] = {}
                distances[addresses[i]][addresses[j]] = dist
                distances[addresses[j]][addresses[i]] = dist

        # Resolver o Problema do Caixeiro Viajante (TSP) e encontrar a melhor rota
        shortest_path, min_distance = solve_tsp(distances, start_address)

        st.subheader(f"A melhor rota começando em '{start_address}' é:")
        st.write(" -> ".join(shortest_path))
       
        # Dividindo a rota em grupos de 10 pontos para o Google Maps
        route_chunks = [shortest_path[i:i+10] for i in range(0, len(shortest_path), 10)]

        # Gerar e exibir os links do Google Maps
        for i, chunk in enumerate(route_chunks):
            link = generate_google_maps_link(chunk)
            st.write(f"Link para a rota {i+1}: [Google Maps]({link})")

# Chama a função principal de execução
if __name__ == "__main__":
    calculate_route()
