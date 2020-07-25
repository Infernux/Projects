type True = Integer
type False = Integer
data MyBool = True | False deriving (Eq)

if' :: MyBool -> a -> a -> a
if' Main.True x _ = x
if' Main.False _ y = y

-- data enum = Something | Someotherthing

-- data TestType a = Integer a a

inc n = n+1
inc :: Integer->Integer

take :: [Char]
take = "Haskell2"

len :: [Char] -> Integer
len [] = 0
len (x:xs) = len xs + 1

head :: [a] -> a
head (x:xs) = x

isEmpty :: [a] -> MyBool
isEmpty [] = Main.True
isEmpty (a) = Main.False

subtail :: [a] -> [a]
subtail (x:xs) = if isEmpty(xs) == Main.True then x:[] else Main.subtail(xs)

tail :: [a] -> a
tail (a) = Main.head(Main.subtail(a))

-- main = putStrLn(show (len (Main.take)))
main = putStrLn(show (Main.tail (Main.take)))
