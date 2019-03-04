data Path = Path
            {roads :: [Road],
             dist  :: Integer} deriving (Show, Eq)

data Road = Road
            {ind  :: Integer,  -- Debugging purpose, adds index to each road added to map
             size :: Integer} deriving (Show, Eq)

-- Roads can be considered to be ordered in sets of 3 as (top left : bottom left : vertical right connecting the two: [...])
data CrossRoad = CrossRoad {connections :: [Road]} deriving (Show)


test_input = [50,10,30, 5,90,20, 40,2,25, 10,8,0]

get_test_map :: [CrossRoad]
get_test_map = city_map (roads_from_input [1..] test_input) []

roads_from_input :: [Integer] -> [Integer] -> [Road]
roads_from_input __ [] = []
roads_from_input (i:ids) (inp:inputs) = (Road i inp : roads_from_input ids inputs)

city_map :: [Road] -> [CrossRoad] -> [CrossRoad]
city_map [] crossroads = crossroads
city_map (r1:r2:r3:roads) [] = city_map roads [start_A, start_B, a, b]
    where start_A = CrossRoad [r1]
          start_B = CrossRoad [r2]
          a = CrossRoad [r1, r3]
          b = CrossRoad [r2, r3]
city_map (r1:r2:r3:roads) crossroads = city_map roads (mod_prev_int ++ [a, b])
    where mod_prev_int = modify_prev crossroads (r1,r2)
          a= CrossRoad [r1, r3]
          b = CrossRoad [r2, r3]

-- Modify the last 2 CrossRoads in the list to add roads
modify_prev :: [CrossRoad] -> (Road, Road) -> [CrossRoad]
modify_prev crosses (r1,r2) = preL ++ [mod_A, mod_B]
    where mod_A = CrossRoad (connections pre_A ++ [r1])
          mod_B = CrossRoad (connections pre_B ++ [r2])
          (preL, pre_A, pre_B) = prev_intersect crosses

-- Return all previous CrossRoads minus the last 2, and the last 2 CrossRoads
prev_intersect :: [CrossRoad] -> ([CrossRoad], CrossRoad, CrossRoad)
prev_intersect crosses = (init $ init crosses, last $ init crosses, last crosses)



join_paths :: Path -> Path -> Path
join_paths p1 p2 = Path (roads p1 ++ (roads p2)) (dist p1 + (dist p2))

calc_path_distance :: Path -> Integer
calc_path_distance p = sum [size x | x <- roads p]

sort_paths :: [Path] -> [Path]
sort_paths (p:paths)= less ++ [p] ++ greater
    where less = sort_paths $ filter (\x -> dist x < dist p) paths
          greater = sort_paths $ filter (\x -> dist x >= dist p) paths

find_paths :: Intersection -> Intersection -> [Path]
find_paths start_cross end_cross =
    where for_each_road =




{-
optimal_paths :: [Integer] -> [Path]
optimal_paths input =
    let result = optimal_paths' $ trace ("\noptimal_paths (input):\n" ++ show input) input
    in trace ("\noptimal_paths (output): " ++ show ++ "\n") result

optimal_paths' input = sort . (\(QuadPaths paths) -> paths) . combine_paths . qp_list $ input
-}