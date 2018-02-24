LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

ENTITY display IS
	PORT(sw0,sw1,sw2,sw3,sw4,sw5,sw6,sw7,sw8,sw9		:IN		STD_LOGIC;
			c0		:OUT 	std_logic_vector(7 downto 0);
			c1		:OUT 	std_logic_vector(7 downto 0);
			c2		:OUT 	std_logic_vector(7 downto 0);
			c3		:OUT 	std_logic_vector(7 downto 0));
END display;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
ENTITY displayComp IS
	PORT( val :IN integer;
				sseg	:OUT    std_logic_vector(7 downto 0));
END displayComp;

ARCHITECTURE displaye OF displayComp IS
BEGIN
	PROCESS (val)
	begin
		case val is
			WHEN 0 =>
                sseg <= "11000000";
				
			WHEN 1 =>
                sseg <= "11111001";
				
			WHEN 2 =>
                sseg <= "10100100";
				
			WHEN 3 =>
                sseg <= "10110000";

			WHEN 4 =>
                sseg <= "10011001";

			WHEN 5 =>
                sseg <= "10010010";

			WHEN 6 =>
                sseg <= "10000010";

			WHEN 7 =>
                sseg <= "11111000";

			WHEN 8 =>
                sseg <= "10000000";

			WHEN 9 =>
                sseg <= "10010000";
				
			WHEN OTHERS =>
				sseg <= "11000000";
		END CASE;
	END PROCESS;

END displaye;

ARCHITECTURE displayArch OF display IS
	
	COMPONENT displayComp
		PORT( val       :IN integer;
			    sseg	:OUT std_logic_vector(7 downto 0));
	END COMPONENT;

	signal val : std_logic_vector(9 downto 0);
	signal digit0,digit1,digit2,digit3 : integer;
	
BEGIN
	AFF1: displayComp port map(digit0,c0);
	AFF2: displayComp port map(digit1,c1);
	AFF3: displayComp port map(digit2,c2);
	AFF4: displayComp port map(digit3,c3);
	val  <= sw9 & sw8 & sw7 & sw6 & sw5 & sw4 & sw3 & sw2 & sw1 & sw0;
	digit0 <= to_integer(unsigned(val)) mod 10;
	digit1 <= to_integer(unsigned(val)) mod 100 / 10;
	digit2 <= to_integer(unsigned(val)) mod 1000 / 100;
	digit3 <= to_integer(unsigned(val)) / 1000;

END displayArch;
