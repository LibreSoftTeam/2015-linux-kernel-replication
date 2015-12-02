USE lkr;

DROP TABLE file;
DROP TABLE lang;
DROP TABLE submodule;
DROP TABLE module;
DROP TABLE version;

CREATE TABLE version
(
id INT NOT NULL,
name VARCHAR(20) NOT NULL,
family VARCHAR(4) NOT NULL,
date DATE,
size INT NOT NULL DEFAULT 0,
PRIMARY KEY (id)
);

CREATE TABLE module
(
id INT NOT NULL,
name VARCHAR(60) NOT NULL,
version_id INT NOT NULL,
PRIMARY KEY (id),
CONSTRAINT fk_version
  FOREIGN KEY (version_id)
  REFERENCES version(id)
);

CREATE TABLE submodule
(
id INT NOT NULL,
name VARCHAR(60) NOT NULL,
module_id INT NOT NULL,
PRIMARY KEY (id),
CONSTRAINT fk_module
  FOREIGN KEY (module_id)
  REFERENCES module(id)
);

CREATE TABLE lang
(
id INT NOT NULL,
name VARCHAR(15) NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE file
(
id INT NOT NULL,
name VARCHAR(50) NOT NULL,
path VARCHAR(100) NOT NULL,
sloc INT NOT NULL,
lang_id INT NOT NULL,
module_id INT NOT NULL,
submodule_id INT NOT NULL,
version_id INT NOT NULL,
PRIMARY KEY (id),
CONSTRAINT fk_lang
  FOREIGN KEY (lang_id)
  REFERENCES lang(id),
CONSTRAINT fk_module_file
    FOREIGN KEY (module_id)
    REFERENCES module(id),
CONSTRAINT fk_submodule_file
      FOREIGN KEY (submodule_id)
      REFERENCES submodule(id),
CONSTRAINT fk_version_file
  FOREIGN KEY (version_id)
  REFERENCES version(id)
);
