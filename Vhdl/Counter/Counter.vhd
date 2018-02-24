LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

entity Counter is
    port(clock      : IN    STD_LOGIC;
            pause   : IN    STD_LOGIC;
            reset   : IN    STD_LOGIC;
			c0		: OUT 	std_logic_vector(7 downto 0);
			c1		: OUT 	std_logic_vector(7 downto 0);
			c2		: OUT 	std_logic_vector(7 downto 0);
			c3		: OUT 	std_logic_vector(7 downto 0));
end Counter;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

architecture CounterCode of Counter is
	COMPONENT displayComp
        PORT(val	: IN	integer;
             sseg	: OUT 	std_logic_vector(7 downto 0));
	END COMPONENT;

    signal s10      : integer := 0;
    signal s1       : integer := 0;
    signal m10      : integer := 0;
    signal m1       : integer := 0;

    signal val2     : integer := 0;
    signal count    : integer := 0;
    signal started  : std_logic := '1';
    signal resetSig : std_logic := '1';

    signal countPath: integer := 0;
begin
    process(clock)
    begin
        if(clock'event and clock='1') then
            if(countPath < 50000000) then
                countPath <= countPath + 1;
            end if;

            if(started = '1' and countPath = 50000000) then
                count <= count + 1;
                countPath <= 0;
            end if;

            if(resetSig = '1') then
                count <= 0;
            end if;
        end if;
    end process;

    process(pause)
    begin
        started <= pause;
    end process;

    process(count)
    begin
        s1 <= count mod 10;
        s10 <= count mod 60 / 10;
        m1 <= count / 60 mod 10;
        m10 <= count / 600;
    end process;

    process(reset)
    begin
        resetSig <= reset;
    end process;

	AFF1: displayComp port map(s1, c0);
	AFF2: displayComp port map(s10, c1);
	AFF3: displayComp port map(m1, c2);
	AFF4: displayComp port map(m10, c3);
end CounterCode;
