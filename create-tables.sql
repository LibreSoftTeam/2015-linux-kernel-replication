
CREATE DATABASE linux_kernel_replication;
USE linux_kernel_replication;

CREATE TABLE versions
(
id INT NOT NULL,
name VARCHAR(20) NOT NULL,
family VARCHAR(4) NOT NULL,
date DATE,
size INT NOT NULL DEFAULT 0,
PRIMARY KEY (id)
);

CREATE TABLE modules
(
id INT NOT NULL,
name VARCHAR(60) NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE submodules
(
id INT NOT NULL,
name VARCHAR(60) NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE langs
(
id INT NOT NULL,
name VARCHAR(15) NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE files
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
  REFERENCES langs(id),
CONSTRAINT fk_module_file
    FOREIGN KEY (module_id)
    REFERENCES modules(id),
CONSTRAINT fk_submodule_file
      FOREIGN KEY (submodule_id)
      REFERENCES submodules(id),
CONSTRAINT fk_version_file
  FOREIGN KEY (version_id)
  REFERENCES versions(id)
);
