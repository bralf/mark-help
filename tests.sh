#!/bin/sh

set -o pipefail

for I in 3-Out/*.txt ; do
  echo "Failed" > "$I" ;
done

runGHC "remove_main.hs" > "2-Work/src1.hs"
mv "2-Work/src1.hs" "2-Work/src.hs"


# PART A -----------------------------------------------------------------------


# 1 :  Numerals

read -r -d '' Q <<'EOF'
main :: IO ()
main = print (numeral 0) >> print (numeral 259)
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans1.txt"




# 2a :  variables

read -r -d '' Q <<'EOF'
main :: IO ()
main = print (map (variables !!) [0,1,2,25,26,51,52,235,732,1020])
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans2a.txt"




# 2b :  filtervariables

read -r -d '' Q <<'EOF'
main :: IO ()
main = print (filterVariables
        ["one","two","three","four","five","six","seven","eight","nine","ten"]
        ["eleven","three","twelve","one","seven","thirteen","nine","five"]
       )
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans2b.txt"



# 2c :  fresh

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print (fresh ["a","b","c","e"])
  print (head $ filterVariables variables ["a","b","c","e"])
  print (fresh ["b","a","e","c"])
  print (head $ filterVariables variables ["b","a","e","c"])
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans2c.txt"




# 2d :  used

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print (used example)
  print (used $ Lambda "a" $ Lambda "b" $ Apply (Variable "c") $ Variable "e")
  print (used $ Lambda "b" $ Lambda "a" $ Apply (Variable "e") $ Variable "c")
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans2d.txt"




# 3a1 :  rename

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ rename "b" "z" example
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans3a1.txt"



# 3a2 :  rename

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ rename "x" "b" $ Apply (Lambda "x" $ Apply (Variable "x") $ Variable "y") $ Apply (Lambda "y" (Variable "x")) $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans3a2.txt"



# 3b1 :  substitute

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ substitute "b" (Lambda "f" $ Lambda "x" $ Variable "x") example
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans3b1.txt"


# 3b2 :  substitute

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ substitute "x" (Apply (Variable "x") (Lambda "a" $ Variable "b")) $ Apply (Lambda "x" $ Variable "x") $ Lambda "y" $ Apply (Variable "a") $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans3b2.txt"


# 3b3 :  substitute

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ substitute "a" (Variable "x") (Lambda "y" $ Variable "y")
  print $ substitute "x" (Apply (Variable "x") (Lambda "a" $ Variable "b")) $ Apply (Lambda "c" $ Apply (Variable "b") $ Variable "x") $ Lambda "x" $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans3b3.txt"



# 4a1 :  beta -- (\x. x) z

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let rdx x = Apply (Lambda "x" $ Variable "x") $ Variable x
  print $ beta $ rdx "z"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4a1.txt"



# 4a2 :  beta -- (\y. (\x. x) y) ((\x. x) z)

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let rdx x = Apply (Lambda "x" $ Variable "x") $ Variable x
  print $ beta $ Apply (Lambda "y" $ rdx "y") $ rdx "z"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4a2.txt"


# 4a3 :  beta -- (\x. x) y ((\x. x) z)

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let rdx x = Apply (Lambda "x" $ Variable "x") $ Variable x
  print $ beta $ Apply (rdx "y") $ rdx "z"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4a3.txt"



# 4a4 :  beta -- \y. (\x. x) y

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let rdx x = Apply (Lambda "x" $ Variable "x") $ Variable x
  print $ beta $ Lambda "y" $ rdx "y"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4a4.txt"



# 4a5 :  beta -- (\x1. \x2. (\x3. x1 x3) x2 ((\x4. x1 x4) x2)) Yes ((\x5. \x6. (\x7. x5 x7) x6 ((\x8. x5 x8) x6)) No)

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = beta $ Apply (Apply (Lambda "x1" $ Lambda "x2" $ Apply (Apply (Lambda "x3" $ Apply (Variable "x1") (Variable "x3")) $ Variable "x2") $ Apply (Lambda "x4" $ Apply (Variable "x1") (Variable "x4")) $ Variable "x2") $ Variable "Yes") $ Apply (Lambda "x5" $ Lambda "x6" $ Apply (Apply (Lambda "x7" $ Apply (Variable "x5") (Variable "x7")) $ Variable "x6") $ Apply (Lambda "x8" $ Apply (Variable "x5") (Variable "x8")) $ Variable "x6") $ Variable "No"
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4a5.txt"



# 4b :  normalize

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = normalize $ Apply (Lambda "x" $ Apply (Apply (Variable "x") $ Variable "is") $ Apply (Lambda "z" $ Variable "z") $ Variable "Sparta!") $ Lambda "y" $ Apply (Variable "This") $ Variable "y"
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4b.txt"



# 4c1 :  normalize -- (\x1. \x2. (\x3. x1 x3) x2 ((\x4. x1 x4) x2)) Yes ((\x5. \x6. (\x7. x5 x7) x6 ((\x8. x5 x8) x6)) No)

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = normalize $ Apply (Apply (Lambda "x1" $ Lambda "x2" $ Apply (Apply (Lambda "x3" $ Apply (Variable "x1") (Variable "x3")) $ Variable "x2") $ Apply (Lambda "x4" $ Apply (Variable "x1") (Variable "x4")) $ Variable "x2") $ Variable "Yes") $ Apply (Lambda "x5" $ Lambda "x6" $ Apply (Apply (Lambda "x7" $ Apply (Variable "x5") (Variable "x7")) $ Variable "x6") $ Apply (Lambda "x8" $ Apply (Variable "x5") (Variable "x8")) $ Variable "x6") $ Variable "No"
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c1.txt"




# 4c2 :  a_normalize

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = (a_normalize $ Apply (Lambda "x" $ Apply (Apply (Lambda "y" $ Apply (Lambda "z" $ Variable "z") $ Variable "x") $ Apply (Lambda "z" $ Apply (Variable "z") $ Variable "x") $ Variable "x") $ Lambda "y" $ Variable "x") $ Apply (Lambda "z" $ Variable "z") $ Variable "y") 
  putStr $ unlines $ map show ts      
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c2.txt"




# 4c3 :  example 1 normal-order

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = normalize example1
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c3.txt"




# 4c4 :  example 1 applicative-order

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = a_normalize example1
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c4.txt"




# 4c5 :  example 2 normal-order

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = normalize example2
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c5.txt"




# 4c6 :  example 2 applicative-order

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let ts = a_normalize example2
  putStr $ unlines $ map show ts
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans4c6.txt"


: '

# PART B -----------------------------------------------------------------------

# 5a :  PState

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print (state1 :: (Term,[Term]))
  print (state1 :: PState)
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5a.txt"




# 5b1 :  p_start

read -r -d '' Q <<'EOF'
main = do
  print $ p_start $ Lambda "x" $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5b1.txt"



# 5b2 :  p_step abstraction

read -r -d '' Q <<'EOF'
main = do
  print $ p_step (Lambda "x" $ Variable "x", [Apply (Variable "One") $ Variable "Two", Variable "Three"])
  print $ substitute "x" (Apply (Variable "One") $ Variable "Two") $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5b2.txt"




# 5b3 :  p_step application

read -r -d '' Q <<'EOF'
main = do
  print $ p_step (Apply (Variable "One") $ Variable "Two", [Variable "Three"])
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5b3.txt"



# 5b4 :  p_final

read -r -d '' Q <<'EOF'
main = do
  print $ p_final (Variable "One" , [Apply (Variable "Two") $ Variable "Three"])
  print $ p_final (Apply (Variable "One") $ Variable "Two", [])
  print $ p_final (Lambda "One" $ Variable "Two" , [])
  print $ p_final (Lambda "One" $ Variable "Two" , [Variable "Three"])
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5b4.txt"



# 5c :  p_run

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  p_run $ Apply (
    Lambda "x" $ Apply (
      Apply (
        Lambda "y" $ Variable "x") $
        Apply (
          Variable "x") $
          Variable "x") $
      Lambda "y" $ Variable "x") $
    Apply (
      Lambda "z" $ Variable "z") $
      Variable "y"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5c.txt"




# 5d :  p_readback

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ p_readback $ (Lambda "This" $ Variable "is", [Apply (Variable "Sparta") $ Variable "!" , Variable "Raaah!"])
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans5d.txt"




# 6a :  Env, State

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print (state2 :: State)
  print (state3 :: State)
  print (state4 :: State)
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6a.txt"




# 6b1 : start

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ start $ Lambda "This" $ Apply (Variable "is") $ Variable "Sparta!"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6b1.txt"




# 6b2 : step

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ step state2
  print $ step state3
  print $ step state4
  print $ step $ step state3
  print $ step $ step state4
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6b2.txt"




# 6b3 : final

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let t = Apply (Variable "One") $ Apply (Variable "Two") $ Variable "Three"
  print $ final $ start t
  print $ final $ step $ start t
  print $ final $ start $ Lambda "One" $ Variable "Two"
  print $ final $ step $ start $ Apply (Lambda "One" $ Variable "Two") $ Variable "Three"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6b3.txt"




# 6c :  run

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  run $ Apply (
    Lambda "x" $ Apply (
      Apply (
        Lambda "y" $ Variable "x") $
        Apply (
          Variable "x") $
          Variable "x") $
      Lambda "z" $ Variable "x") $
    Apply (
      Lambda "z" $ Variable "z") $
      Variable "y"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6c.txt"



# 6d1 :  readback

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let steps 0 = start
      steps n = step . steps (n-1)
  print $ readback state2
  print $ readback state3
  print $ readback state4
  print $ readback $ steps 2 $ Apply (Lambda "x" $ Lambda "y" $ Variable "x") $ Variable "y"
  print $ readback $ steps 4 $ Apply (Apply (Lambda "x" $ Lambda "y" $ Lambda "z" $ Variable "x") $ Variable "y") $ Variable "z"
  print $ readback $ steps 4 $ Apply (Apply (Lambda "y" $ Lambda "x" $ Lambda "z" $ Variable "x") $ Variable "z") $ Variable "y"
  print $ readback $ steps 7 $ Apply (Lambda "a" $ Apply (Lambda "b" $ Apply (Lambda "c" $ Apply (Apply (Variable "c") $ Lambda "b" $ Variable "a") $ Variable "c") $ Variable "b") $ Apply (Variable "a") $ Variable "a") $ Lambda "a" $ Variable "a"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6d1.txt"



# 6d2 :  readback -- 1 2 3

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  print $ readback $ step $ step $ start $ Apply (Apply (Variable "1") $ Variable "2") $ Variable "3"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6d2.txt"



# 6d3 :  readback -- 3 2 1

read -r -d '' Q <<'EOF'
main :: IO ()
main = do
  let steps 0 = start
      steps n = step . steps (n-1)
      xsub x n m = Apply (Lambda x m) n
  print $ readback $ steps 3 $ Apply (Apply (Lambda "y" $ Variable "1") $ Variable "NO") $ Variable "y"
  print $ readback $ steps 8 $ xsub "x" (Variable "1") $ xsub "y" (Variable "2") $ xsub "z" (Variable "3") $ Apply (Apply (Variable "z") $ Variable "y") $ Variable "x"
  print $ readback $ steps 8 $ xsub "x" (Variable "1") $ Apply (xsub "x" (Variable "2") $ Apply (xsub "x" (Variable "3") $ (Variable "x")) $ Variable "x") $ Variable "x"
EOF

cp "2-Work/src.hs" "2-Work/temp.hs"
echo "$Q" >> "2-Work/temp.hs"

runGHC "2-Work/temp.hs" > "3-Out/ans6d3.txt"
'
