library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity VGA is
  port(clock  : in std_logic;
       red   : out std_logic_vector(3 downto 0);
       green : out std_logic_vector(3 downto 0);
       blue  : out std_logic_vector(3 downto 0);
       hsync    : out std_logic;
       vsync    : out std_logic);
end VGA;

architecture Behavioral of VGA is

signal clk25              : std_logic;
signal horizontal_counter : std_logic_vector (9 downto 0);
signal vertical_counter   : std_logic_vector (9 downto 0);

begin

-- generate a 25Mhz clock
process (clock)
begin
  if clock'event and clock='1' then
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
      red <= "1111";
      blue <= "0000";
      green <= "0000";
    else
      red <= "0000";
      green <= "0000";
      blue <= "0000";
    end if;
    if (horizontal_counter > "0000000000" )
      and (horizontal_counter < "0001100001" ) -- 96+1
    then
      hsync <= '0';
    else
      hsync <= '1';
    end if;
    if (vertical_counter > "0000000000" )
      and (vertical_counter < "0000000011" ) -- 2+1
    then
      vsync <= '0';
    else
      vsync <= '1';
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
