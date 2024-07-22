create table customer( 
    customer_id int(255) not null auto_increment,
    name text not null, 
    surname text not null,
    username text not null,
    password text not null, 
    admin boolean default FALSE,
    primary key (customer_id)
);


create table drink_base (
    base_id int(255) not null auto_increment,
    description text not null,
    primary key (base_id)
);

create table drink_flavour (
    flavour_id int(255) not null auto_increment,
    description text not null,
    base_id int(255) not null,
    primary key (flavour_id),
    foreign key (base_id) references drink_base(base_id)
);

create table drink_popping (
    popping_id int(255) not null auto_increment,
    description text not null,
    base_id int(255) not null,
    primary key (popping_id),
    foreign key (base_id) references drink_base(base_id)
);

create table product (
    purchase_id int(255) not null auto_increment,
    customer_id int(255) not null,
    base_id int(255) not null,
    flavour_id int(255) not null,
    popping_id int(255) not null,
    sugar int(255) not null,
    size int(255) not null,
    price int(255) not null,
    purchase_date datetime not null,
    primary key (purchase_id),
    foreign key (customer_id) references customer(customer_id),
    foreign key (base_id) references drink_base(base_id),
    foreign key (flavour_id) references drink_flavour(flavour_id),
    foreign key (popping_id) references drink_popping(popping_id)
);


