CREATE TABLE zemp_hike(emp_id BIGINT,title_id VARCHAR(15),rating_id VARCHAR(15),hike_amt INT,skill_id VARCHAR(15),finance_id VARCHAR(15),FOREIGN KEY(emp_id) REFERENCES employee(emp_id),FOREIGN KEY(title_id) REFERENCES titles(title_id),FOREIGN KEY(rating_id) REFERENCES rating(rating_id),FOREIGN KEY(skill_id) REFERENCES skill_set(skill_id),FOREIGN KEY(finance_id) REFERENCES financial_year(finance_id));