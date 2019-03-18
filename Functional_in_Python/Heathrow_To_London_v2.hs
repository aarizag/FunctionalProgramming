-- Data type denoting a Path: series of roads and a total distance covered
data Path = Path
            {roads :: [Integer],
             dist  :: Integer} deriving (Show, Eq)

-- Data type describing each road with the time it takes to traverse it, an ID number, and a value denoting its location (A, B, V)
-- This is currently unused
data Road = Road
            {time :: Integer,
             iden :: Integer,
             val :: String} deriving (Show)

-- Test Input given in 3s visualized sas (top left : bottom left : vertical right connecting the two: [...])
test_input = [50,10,30, 5,90,20, 40,2,25, 10,8,0]
test_input2 = [15,5,10, 10,30,10, 5,20,5, 35,15,20, 15,10,0]

-- Test the optimal path algorithm with the test input
optimal_path_test = min_p (fst opt) (snd opt)
    where opt = optimal_path test_input (Path [] 0, Path [] 0)
optimal_path_test2 = min_p (fst opt) (snd opt)
    where opt = optimal_path test_input2 (Path [] 0, Path [] 0)


{-
Find the optimal path from Heathrow to London utilizing the test input
:@where var:
    join_p = the new set of best paths to combined with the previous best paths to A/B respectively
    (a,b) = the 2 best paths to A/B given a new set of 3 roads
:@param:
    (rT:rB:rV:roads) = top road, bottom road, vertical road, and the remainder of all roads

-}
optimal_path :: [Integer] -> (Path,Path) -> (Path,Path)
optimal_path [] (a,b) = (a,b)
optimal_path (rT:rB:rV:roads) (old_a, old_b) = optimal_path roads join_paths
    where join_paths = combine old_a old_b a b rT
          (a,b) = find_best $ quad_path rT rB rV

{-
Find the best paths to Point A (top intersection) and B (bottom intersection) by comparing all possible routes
per set of 3 roads
:@where var:
    best_A/best_B = the shortest path, given the current 3 roads, to A/B respectively
-}
find_best :: (Path, Path, Path, Path) -> (Path, Path)
find_best (a_from_a, b_from_a, a_from_b, b_from_b) = (best_A, best_B)
    where best_A = min_p a_from_a a_from_b  -- best path to a
          best_B = min_p b_from_a b_from_b  -- best path to b

-- Compare 2 paths and return shorter one
min_p :: Path -> Path -> Path
min_p p1 p2 = if dist p1 < dist p2 then p1 else p2  -- compare 2 paths and return shorter one
,
{-
Combine the old best routes with the new best routes.
Considers what street the new route is starting on and where the old route left off

@:where var:
    com_a/com_b = the new best path to a/b combined with an old path
        the old path is determined by seeing whether or not the new path starts on the top road
-}
combine :: Path -> Path -> Path -> Path -> Integer -> (Path, Path)
combine old_a old_b a b rT = (com_a, com_b)
    where
        com_a = if (head $ roads a) == rT
                then Path (roads old_a ++ (roads a)) (dist old_a + (dist a))
                else Path (roads old_b ++ (roads a)) (dist old_b + (dist a))
        com_b = if (head $ roads b) == rT
                then Path (roads old_a ++ (roads b)) (dist old_a + (dist b))
                else Path (roads old_b ++ (roads b)) (dist old_b + (dist b))

{-
Return Tuple of All Paths:
(A -> A1, A -> B1, B -> A1, B -> B1)
-}
quad_path :: Integer -> Integer -> Integer -> (Path, Path, Path, Path)
quad_path rT rB rV = (a1, a2, b1, b2)
    where a1 = Path [rT] rT
          a2 = Path [rT, rV] (rT+rV)
          b1 = Path [rB, rV] (rB+rV)
          b2 = Path [rB] rB
--    where a = if r1 == starting_road then Path [r1] r1 else Path [r2, r3] (r2+r3)
--          b = if r1 == starting_road then Path [r1, r3] (r1+r3) else Path [r2] r2
