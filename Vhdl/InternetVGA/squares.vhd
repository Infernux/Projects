library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity clockmodule is
  port(clk50_in  : in std_logic;
       red_out   : out std_logic;
       green_out : out std_logic;
       blue_out  : out std_logic;
       hs_out    : out std_logic;
       vs_out    : out std_logic);
end clockmodule;

architecture Behavioral of clockmodule is

signal clk25              : std_logic;
signal horizontal_counter : std_logic_vector (9 downto 0);
signal vertical_counter   : std_logic_vector (9 downto 0);

begin

-- generate a 25Mhz clock
process (clk50_in)
begin
  if clk50_in'event and clk50_in='1' then
    if (clk25 = '0') then
      clk25 <= '1';
    else
      clk25 <= '0';
    end if;
  end if;
end process;

process (clk25) 
begin
  if clk25'event and clk25 = '1' then
    if (horizontal_counter >= "0010010000" ) -- 144
    and (horizontal_counter < "1100010000" ) -- 784
    and (vertical_counter >= "0000100111" ) -- 39
    and (vertical_counter < "1000000111" ) -- 519
    then
      red_out <= horizontal_counter(3) 
	            and vertical_counter(3);
      green_out <= horizontal_counter(4) 
	            and vertical_counter(4);
      blue_out <= horizontal_counter(5) 
	            and vertical_counter(5);
    else
      red_out <= '0';
      green_out <= '0';
      blue_out <= '0';
    end if;
    if (horizontal_counter > "0000000000" )
      and (horizontal_counter < "0001100001" ) -- 96+1
    then
      hs_out <= '0';
    else
      hs_out <= '1';
    end if;
    if (vertical_counter > "0000000000" )
      and (vertical_counter < "0000000011" ) -- 2+1
    then
      vs_out <= '0';
    else
      vs_out <= '1';
    end if;
    horizontal_counter <= horizontal_counter+"0000000001";
    if (horizontal_counter="1100100000") then
      vertical_counter <= vertical_counter+"0000000001";
      horizontal_counter <= "0000000000";
    end if;
    if (vertical_counter="1000001001") then		    
      vertical_counter <= "0000000000";
    end if;
  end if;
end process;

end Behavioral;
