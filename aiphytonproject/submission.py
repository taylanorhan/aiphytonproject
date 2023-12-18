
import csv
import heapq



class FileNotFoundError(Exception):
    pass


class CityNotFoundError(Exception):
    pass

file_path = 'cities.csv'

def read_road_map(file_path):
    road_map = {}
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                city1, city2, distance = row
                if city1 not in road_map:
                    road_map[city1] = {}
                if city2 not in road_map:
                    road_map[city2] = {}
                road_map[city1][city2] = int(distance)
                road_map[city2][city1] = int(distance)
    except FileNotFoundError:
        raise FileNotFoundError("Road map file not found.")
    return road_map


def find_shortest_path(road_map, start_city, target_city):
    queue = [
        (0, start_city, [])
    ]  
    visited = set()

    while queue:
        cost, current_city, path = heapq.heappop(
            queue
        )  
        path = path + [current_city]

        if current_city == target_city:
            return cost, path

        if current_city not in visited:
            visited.add(current_city)
            neighbors = road_map[current_city]
            for neighbor, distance in neighbors.items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + distance, neighbor, path))


def handle_exceptions(file_path, start_city, target_city):
    try:
        road_map = read_road_map(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("Road map file not found.")

    if start_city not in road_map:
        raise CityNotFoundError(f"Start city '{start_city}' not found in the road map.")

    if target_city not in road_map:
        raise CityNotFoundError(
            f"Target city '{target_city}' not found in the road map."
        )

    return road_map


def get_user_input(prompt):
    while True:
        user_input = input(prompt)
        if (
            user_input.strip()
        ):  
            return user_input.strip()
        else:
            print("Input cannot be empty. Please enter again.")


def main():
    print("Welcome to the Shortest Path Finder!")
    while True:
        try:
            file_path = get_user_input("Enter the path of the road map file: ")
            start_city = get_user_input("Enter the start city: ")
            target_city = get_user_input("Enter the target city: ")

            road_map = handle_exceptions(file_path, start_city, target_city)
            cost, path = find_shortest_path(road_map, start_city, target_city)
            print(
                f"The shortest path from {start_city} to {target_city} is: {' -> '.join(path)}"
            )
            print(f"The distance is: {cost}")

            break  
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")
            print("Please provide a valid file path.")
        except CityNotFoundError as e:
            print(f"Error: {str(e)}")
            print("Please enter valid start and target cities.")


if __name__ == "__main__":
    main()