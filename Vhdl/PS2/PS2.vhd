LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

entity PS2 is
    port(kbclock    : IN STD_LOGIC;
            kbdata  : IN STD_LOGIC;
			c0		: OUT 	std_logic_vector(7 downto 0);
			c1		: OUT 	std_logic_vector(7 downto 0);
			c2		: OUT 	std_logic_vector(7 downto 0);
			c3		: OUT 	std_logic_vector(7 downto 0));
end ps2;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

architecture PS2Code of PS2 is
	COMPONENT display
        PORT(val	: IN	integer;
             c0		: OUT 	std_logic_vector(7 downto 0);
             c1		: OUT 	std_logic_vector(7 downto 0);
             c2		: OUT 	std_logic_vector(7 downto 0);
             c3		: OUT 	std_logic_vector(7 downto 0));
	END COMPONENT;

    signal val      : integer;
    signal tmp      : std_logic_vector(0 to 15) := "0000000000000000";
    signal count    : integer := 0;

    signal state    : integer := 0;
    signal parity   : std_logic := '0';
begin
    process(kbclock)
    begin
        if(kbclock'event and kbclock='0') then
            if(state=0 and kbdata='0') then
                ---begin
                state <= 1;
            elsif(state=1) then
                if(count=7 or count=15) then
                    state <= 2;
                end if;
                tmp(15-count) <= kbdata;
                count <= count + 1;
                ---newValue <= kbdata;
            elsif(state=2) then
                ---parity
                state <= 3;
                parity <= kbdata;
            elsif(state=3 and kbdata='1') then
                ---end
                state <= 0;
                if(count=16) then
                    count <= 0;
                end if;

                if(not(tmp(0) xor tmp(1) xor tmp(2) xor tmp(3) xor tmp(4) xor tmp(5) xor tmp(6) xor tmp(7)) = parity) then
                    val <= to_integer(unsigned(tmp));
                end if;
            end if;
        end if;
    end process;

    ---process(newValue)
    ---begin
    ---    ready <= '0';
    ---    count <= count + 1;
    ---    tmp <= newValue & tmp(15 DOWNTO 1);
    ---    if(count=8) then
    ---        ready <= '1';
    ---        count <= 0;
    ---    end if;
    ---end process;

---    process(ready)
---    begin
---        if(ready'event and ready='1') then
---            val <= to_integer(unsigned(tmp));
---        end if;
---    end process;

	AFF: display port map(val, c0, c1, c2, c3);
end PS2Code;
