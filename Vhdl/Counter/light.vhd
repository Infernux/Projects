LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

ENTITY display IS
	PORT(val		:IN		integer;
			c0		:OUT 	std_logic_vector(7 downto 0);
			c1		:OUT 	std_logic_vector(7 downto 0);
			c2		:OUT 	std_logic_vector(7 downto 0);
			c3		:OUT 	std_logic_vector(7 downto 0));
END display;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

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

	signal digit0,digit1,digit2,digit3 : integer;
	
BEGIN
	AFF1: displayComp port map(digit0,c0);
	AFF2: displayComp port map(digit1,c1);
	AFF3: displayComp port map(digit2,c2);
	AFF4: displayComp port map(digit3,c3);
	digit0 <= val mod 10;
	digit1 <= val mod 100 / 10;
	digit2 <= val mod 1000 / 100;
	digit3 <= val / 1000;

END displayArch;
