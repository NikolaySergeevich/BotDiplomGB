USE botgb;
CREATE TABLE users
(id INT AUTO_INCREMENT PRIMARY KEY,
user_id VARCHAR(25) NOT NULL,
date_add_user DATE NOT NULL,
date_content_test DATETIME NULL,
link_data_test VARCHAR(150) NULL,
link_data_compare_developer VARCHAR(200) NULL,
link_data_compare_tester VARCHAR(200) NULL,
link_data_compare_analist VARCHAR(200) NULL,
link_data_compare_project VARCHAR(200) NULL,
link_data_compare_prodact VARCHAR(200) NULL,
link_finish_img VARCHAR(150) NULL,
indicate TINYINT(1) DEFAULT 0);
CREATE TABLE capabilities
(id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
extrovert TINYINT(1) UNSIGNED DEFAULT 0,
introvert TINYINT(1) UNSIGNED DEFAULT 0,
ability_to_work_monotonously TINYINT(1) UNSIGNED DEFAULT 0,
mentoring TINYINT(1) UNSIGNED DEFAULT 0,
analytical_skills TINYINT(1) UNSIGNED DEFAULT 0,
empathy TINYINT(1) UNSIGNED DEFAULT 0,
curiosity TINYINT(1) UNSIGNED DEFAULT 0,
oratory TINYINT(1) UNSIGNED DEFAULT 0,
organizational_skills TINYINT(1) UNSIGNED DEFAULT 0,
critical_thinking TINYINT(1) UNSIGNED DEFAULT 0,
multitasking TINYINT(1) UNSIGNED DEFAULT 0,
creativity TINYINT(1) UNSIGNED DEFAULT 0,
stress_resistance TINYINT(1) UNSIGNED DEFAULT 0,
time_control TINYINT(1) UNSIGNED DEFAULT 0,
working_with_a_large_amount_of_information TINYINT(1) UNSIGNED DEFAULT 0,
sum_general_bals TINYINT UNSIGNED DEFAULT 0,
sum_bals_compare_with_developer TINYINT UNSIGNED DEFAULT 0,
sum_bals_compare_with_tester TINYINT UNSIGNED DEFAULT 0,
sum_bals_compare_with_analist TINYINT UNSIGNED DEFAULT 0,
sum_bals_compare_with_prodact TINYINT UNSIGNED DEFAULT 0,
sum_bals_compare_with_project TINYINT UNSIGNED DEFAULT 0,
FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (user_id, date_add_user) VALUES ('developer', NOW());
INSERT INTO users (user_id, date_add_user) VALUES ('tester', NOW());
INSERT INTO users (user_id, date_add_user) VALUES ('analist', NOW());
INSERT INTO users (user_id, date_add_user) VALUES ('project', NOW());
INSERT INTO users (user_id, date_add_user) VALUES ('prodact', NOW());

INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = 'developer');
INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = 'tester');
INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = 'analist');
INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = 'project');
INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = 'prodact');

UPDATE capabilities SET `extrovert` = '2', `introvert` = '3', `ability_to_work_monotonously` = '4', `mentoring` = '0', `analytical_skills` = '4', `empathy` = '2', `curiosity` = '5', `oratory` = '0', `organizational_skills` = '1', `critical_thinking` = '3', `multitasking` = '3', `creativity` = '1', `stress_resistance` = '4', `time_control` = '3', `working_with_a_large_amount_of_information` = '5' WHERE (`id` = '1');
UPDATE capabilities SET `extrovert` = '2', `introvert` = '2', `ability_to_work_monotonously` = '5', `mentoring` = '0', `analytical_skills` = '3', `empathy` = '3', `curiosity` = '4', `oratory` = '0', `organizational_skills` = '1', `critical_thinking` = '3', `multitasking` = '3', `creativity` = '1', `stress_resistance` = '2', `time_control` = '3', `working_with_a_large_amount_of_information` = '3' WHERE (`id` = '2');
UPDATE capabilities SET `extrovert` = '3', `introvert` = '4', `ability_to_work_monotonously` = '3', `mentoring` = '0', `analytical_skills` = '5', `empathy` = '2', `curiosity` = '4', `oratory` = '1', `organizational_skills` = '2', `critical_thinking` = '5', `multitasking` = '3', `creativity` = '3', `stress_resistance` = '3', `time_control` = '2', `working_with_a_large_amount_of_information` = '4' WHERE (`id` = '3');
UPDATE capabilities SET `extrovert` = '4', `introvert` = '1', `ability_to_work_monotonously` = '1', `mentoring` = '3', `analytical_skills` = '3', `empathy` = '4', `curiosity` = '3', `oratory` = '4', `organizational_skills` = '5', `critical_thinking` = '3', `multitasking` = '5', `creativity` = '3', `stress_resistance` = '5', `time_control` = '5', `working_with_a_large_amount_of_information` = '4' WHERE (`id` = '4');
UPDATE capabilities SET `extrovert` = '3', `introvert` = '2', `ability_to_work_monotonously` = '3', `mentoring` = '3', `analytical_skills` = '3', `empathy` = '4', `curiosity` = '2', `oratory` = '4', `organizational_skills` = '4', `critical_thinking` = '3', `multitasking` = '5', `creativity` = '2', `stress_resistance` = '4', `time_control` = '4', `working_with_a_large_amount_of_information` = '3' WHERE (`id` = '5');

UPDATE capabilities SET sum_general_bals = extrovert + introvert + ability_to_work_monotonously + mentoring + analytical_skills + empathy + curiosity + oratory + organizational_skills + critical_thinking + multitasking + creativity + stress_resistance + time_control + working_with_a_large_amount_of_information;


DELIMITER //
CREATE PROCEDURE check_exists_user (IN IdUser VARCHAR(25))
BEGIN
	SELECT EXISTS(SELECT user_id FROM users WHERE user_id = IdUser) AS item;
END//
DELIMITER ;
CALL check_exists_user ('developer');
DELIMITER //

CREATE PROCEDURE AddUser (IN IdUser VARCHAR(25))
BEGIN
	INSERT INTO users (user_id, date_add_user) SELECT IdUser, NOW()
	WHERE
	NOT EXISTS (SELECT user_id FROM users WHERE user_id = IdUser);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddUserincat (IN IdUser VARCHAR(25))
BEGIN
	INSERT INTO capabilities (user_id) SELECT (SELECT id FROM users WHERE user_id = IdUser)
	WHERE
	NOT EXISTS (SELECT user_id FROM capabilities WHERE user_id = (SELECT id FROM users WHERE user_id = IdUser));

END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE check_passed_the_test (IN IdUser VARCHAR(25))
BEGIN
	SELECT indicate
    FROM users
    WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_degry (IN column_names VARCHAR(50), IN IdUser VARCHAR(25), IN degry TINYINT(1))
BEGIN
    SET @update_d:=CONCAT("UPDATE capabilities SET ",column_names," = ",degry," WHERE  user_id = (SELECT id FROM users WHERE user_id = ",IdUser,")");
    SELECT @update_d;
    PREPARE update_degry FROM @update_d;
    EXECUTE update_degry;
    DEALLOCATE PREPARE update_degry;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_indicate_user (IN IdUser VARCHAR(25), IN new_indicate TINYINT(1))
BEGIN
	UPDATE users SET indicate = new_indicate WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_value_capabilities (IN IdUser VARCHAR(25))
BEGIN
	SELECT *
    FROM capabilities
    WHERE user_id = (SELECT id FROM users WHERE user_id = IdUser);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE giv_volues_compare (IN column_names VARCHAR(50), IN IdUser VARCHAR(25))
BEGIN
	SET @stlect_vol:=CONCAT("SELECT ",column_names," FROM capabilities WHERE  user_id = (SELECT id FROM users WHERE user_id = ",IdUser,")");
    PREPARE select_vol FROM @stlect_vol;
    EXECUTE select_vol;
    DEALLOCATE PREPARE select_vol;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_finish_img (IN IdUser VARCHAR(25), IN link VARCHAR(150))
BEGIN
	UPDATE users SET link_finish_img = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_time_content_test (IN IdUser VARCHAR(25))
BEGIN
	UPDATE users SET date_content_test = NOW() WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_test (IN IdUser VARCHAR(25), IN link VARCHAR(150))
BEGIN
	UPDATE users SET link_data_test = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_compare_developer (IN IdUser VARCHAR(25), IN link VARCHAR(200))
BEGIN
	UPDATE users SET link_data_compare_developer = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_compare_tester (IN IdUser VARCHAR(25), IN link VARCHAR(200))
BEGIN
	UPDATE users SET link_data_compare_tester = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_compare_analist (IN IdUser VARCHAR(25), IN link VARCHAR(200))
BEGIN
	UPDATE users SET link_data_compare_analist = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_compare_prodact (IN IdUser VARCHAR(25), IN link VARCHAR(200))
BEGIN
	UPDATE users SET link_data_compare_prodact = link WHERE user_id = IdUser;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_link_data_compare_project (IN IdUser VARCHAR(25), IN link VARCHAR(200))
BEGIN
	UPDATE users SET link_data_compare_project = link WHERE user_id = IdUser;
END//
DELIMITER ;