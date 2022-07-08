create table if not exists auth_group
(
    id   int auto_increment
        primary key,
    name varchar(150) not null,
    constraint name
        unique (name)
);

create table if not exists django_content_type
(
    id        int auto_increment
        primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

create table if not exists auth_permission
(
    id              int auto_increment
        primary key,
    name            varchar(255) not null,
    content_type_id int          not null,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename),
    constraint auth_permission_content_type_id_2f476e4b_fk_django_co
        foreign key (content_type_id) references django_content_type (id)
);

create table if not exists auth_group_permissions
(
    id            bigint auto_increment
        primary key,
    group_id      int not null,
    permission_id int not null,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id),
    constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
        foreign key (permission_id) references auth_permission (id),
    constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
        foreign key (group_id) references auth_group (id)
);

create table if not exists django_migrations
(
    id      bigint auto_increment
        primary key,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime(6)  not null
);

create table if not exists django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data longtext    not null,
    expire_date  datetime(6) not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table if not exists user_user
(
    last_login datetime(6)  null,
    id         bigint auto_increment
        primary key,
    email      varchar(100) not null,
    password   varchar(128) not null,
    username   varchar(20)  not null,
    mobile     varchar(20)  not null,
    is_active  tinyint(1)   not null,
    is_admin   tinyint(1)   not null,
    created_at datetime(6)  not null,
    updated_at datetime(6)  not null,
    constraint email
        unique (email)
);

create table if not exists account_book_accountbook
(
    created_at datetime(6) not null,
    updated_at datetime(6) not null,
    id         bigint auto_increment
        primary key,
    title      varchar(20) not null,
    balance    int         not null,
    is_deleted tinyint(1)  not null,
    user_id    bigint      not null,
    deleted_at datetime(6) null,
    constraint account_book_accountbook_user_id_c1b40ef0_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists account_book_accountbookrecord
(
    created_at      datetime(6)  not null,
    updated_at      datetime(6)  not null,
    id              bigint auto_increment
        primary key,
    amount          int          not null,
    memo            varchar(100) not null,
    is_deleted      tinyint(1)   not null,
    account_book_id bigint       not null,
    date            date         not null,
    deleted_at      datetime(6)  null,
    constraint account_book_account_account_book_id_8bb462e3_fk_account_b
        foreign key (account_book_id) references account_book_accountbook (id)
);

create table if not exists django_admin_log
(
    id              int auto_increment
        primary key,
    action_time     datetime(6)       not null,
    object_id       longtext          null,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  longtext          not null,
    content_type_id int               null,
    user_id         bigint            not null,
    constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
        foreign key (content_type_id) references django_content_type (id),
    constraint django_admin_log_user_id_c564eba6_fk_user_user_id
        foreign key (user_id) references user_user (id),
    check (`action_flag` >= 0)
);

