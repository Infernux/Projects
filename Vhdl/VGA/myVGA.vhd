LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

entity VGA is
    port(clock      : IN STD_LOGIC;
         hsync      : OUT STD_LOGIC;
         vsync      : OUT STD_LOGIC;
         red        : OUT std_logic_vector(3 downto 0);
         blue       : OUT std_logic_vector(3 downto 0);
         green      : OUT std_logic_vector(3 downto 0)
        );
end vga;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

architecture VGACode of VGA is
    signal clock25  : std_logic := '0';

    signal started  : std_logic := '0';
    signal ready    : std_logic := '1';

    signal displayH : integer   := 0;
    signal displayV : integer   := 0;

    signal Hstate    : integer   := 0;
    signal Vstate    : integer   := 0;

    signal counter  : std_logic := '0';
    signal vertStep : integer   := 0;

    constant WRes: integer := 640;
    constant WfrontPorch: integer := 16;
    constant Wsync: integer := 96;
    constant WbackPorch: integer := 48;

    constant VerRes: integer := 480;
    constant VerfrontPorch: integer := 2;
    constant Versync: integer := 2;
    constant VerbackPorch: integer := 37;

begin
    process(clock)
    begin
        if(clock'event and clock='1') then
            clock25<=not clock25;
        end if;
        if(clock25='1') then
            displayH <= displayH + 1;
            ---cas display
            if(Hstate=0) then
                if(Vstate=0) then
                    red<="1111";
                    blue<="0000";
                    green<="0000";
                end if;
                if(displayH>=WRes) then
                    Hstate <= 1;
                    displayH <= 0;
                end if;
            ---cas front porch
            elsif(Hstate=1) then
                red<="0000";
                blue<="0000";
                green<="0000";
                if(displayH>=WfrontPorch) then
                    Hstate <= 2;
                    displayH <= 0;
                end if;
            ---cas sync
            elsif(Hstate=2) then
                red<="0000";
                blue<="0000";
                green<="0000";
                hsync <= '0';
                if(displayH>=Wsync) then
                    Hstate <= 3;
                    displayH <= 0;
                end if;
            ---cas back porch
            elsif(Hstate=3) then
                red<="0000";
                blue<="0000";
                green<="0000";
                hsync <= '1';
                if(displayH>=WbackPorch) then
                    Hstate <= 0;
                    displayH <= 0;
                    vertStep <= vertStep+1;
                    ---cas display
                    if(Vstate=0) then
                        if(vertStep>=VerRes) then
                            Vstate <= 1;
                            vertStep <= 0;
                        end if;
                    ---cas front porch
                    elsif(Vstate=1) then
                        if(vertStep>=VerfrontPorch) then
                        ---if(vertStep>=489) then
                            Vstate <= 2;
                            vertStep <= 0;
                        end if;
                    ---cas sync
                    elsif(Vstate=2) then
                        vsync <= '0';
                        if(vertStep>=VerSync) then
                        ---if(vertStep>=491) then
                            Vstate <= 3;
                            vertStep <= 0;
                        end if;
                    ---cas back porch
                    elsif(Vstate=3) then
                        vsync <= '1';
                        if(vertStep>=VerbackPorch) then
                        ---if(vertStep>=524) then
                            Vstate <= 0;
                            vertStep <= 0;
                        end if;
                    end if;
                end if;
            end if;
        end if;
    end process;

--- process(displayH)
---    begin
---        if(Hstate=3) then
---            red<="0000";
---            blue<="0000";
---            green<="0000";
---        else
---            red<="1111";
---            blue<="0000";
---            green<="0000";
---        end if;
---    end process;
end VGACode;
