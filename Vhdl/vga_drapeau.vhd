LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY vga_test IS
PORT(   
		clk : IN STD_LOGIC;
		hsync,
		vsync : out std_logic;
		red :  out  STD_LOGIC_VECTOR(3 DOWNTO 0);
		green :  out  STD_LOGIC_VECTOR(3 DOWNTO 0);
		blue :  out  STD_LOGIC_VECTOR(3 DOWNTO 0)
);
end vga_test;

ARCHITECTURE behavior of vga_test IS
	SIGNAL 	h_sync, v_sync,clock	:	STD_LOGIC;
	SIGNAL 	video_en, 	
		horizontal_en, 
		vertical_en	: STD_LOGIC;
	SIGNAL	red_signal , green_signal, blue_signal : STD_LOGIC_VECTOR(3 DOWNTO 0);
	SIGNAL 	h_cnt, 
		v_cnt : STD_LOGIC_VECTOR(9 DOWNTO 0);	
BEGIN
	video_en <= horizontal_en AND vertical_en;

	PROCESS
	BEGIN
		WAIT UNTIL(clk'EVENT) AND (clk = '1');
		if(clock = '1') then
			clock <= '0';
		else 
			clock <= '1';
		end if;
	
		if(clock = '1') then 	
			IF (h_cnt = 794) THEN
				h_cnt <= "0000000000";
			ELSE
				h_cnt <= h_cnt + 1;
			END IF;

			IF (h_cnt >= 0) AND (h_cnt <= 213) THEN
				red_signal <= "0000";
				green_signal <= "0000";
				blue_signal <= "1111";
			END IF;	
	
			IF (h_cnt >= 214) AND (h_cnt <= 428) THEN
				red_signal <= "1111";
				green_signal <= "1111";
				blue_signal <= "1111";	
			END IF;	
	
			IF (h_cnt >= 429) AND (h_cnt <= 639) THEN
				red_signal <= "0000";
				green_signal <= "1111";
				blue_signal <= "0000";			
			END IF;
	
			IF (h_cnt <= 751) AND (h_cnt >= 655) THEN
				h_sync <= '0';
			ELSE
				h_sync <= '1';
			END IF;
	
			IF (v_cnt >= 524) AND (h_cnt >= 794) THEN
				v_cnt <= "0000000000";
			ELSIF (h_cnt = 794) THEN
				v_cnt <= v_cnt + 1;
			END IF;
	
			IF (v_cnt <= 491) AND (v_cnt >= 489) THEN
				v_sync <= '0';		
			ELSE
				v_sync <= '1';
			END IF;
	
			IF (h_cnt <= 639) THEN
				horizontal_en <= '1';
			ELSE
				horizontal_en <= '0';
			END IF;
	
			IF (v_cnt <= 479) THEN
				vertical_en <= '1';
			ELSE
				vertical_en <= '0';
			END IF;
		end if;
	
		if(video_en = '1') then
			red	<= red_signal;
			green   <= green_signal;
			blue	<= blue_signal;
		else
			red <= "0000";
			green <= "0000";
			blue <= "0000";
		end if;
	
		hsync	<= h_sync;
		vsync	<= v_sync;
	END PROCESS;
END behavior;
