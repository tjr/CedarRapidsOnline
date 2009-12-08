-- SQL Tables for CedarRapidsOnline web service
-- Copyright (C) 2009 Clear Perception Solutions, LLC.
-- Written by Trevis J. Rothwell <tjr@gnu.org>
--
-- This file is part of the CedarRapidsOnline web service.
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
-- 
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------

-- users
-- Holds data for each registered user:
--   user_id: 	  Serial, auto-generated key value
--   name: 	  User's (real) name, as displayed in postings
--   email:	  User's email address
--   password:	  User's password (should be stored encrypted)
--   level:	  User's access level...
--   		  0 : disabled user account
--		  1 : regular user
--		  2 : admin user
--   url:	  User's website (can be null)
--   registration_date:	 Timestamp of when user account was created
--
create table users (
       user_id			serial primary key,
       name			varchar(100) not null,
       email			varchar (100) not null unique,
       password			varchar (50) not null,
       level			int4 not null,
       url			text,
       registration_date	timestamp (0)
);


-- articles
-- Holds data for each article:
--   article_id:       Serial, auto-generated key value
--   refers_to:	       Parent article_id.  can be null, which indicates
--   		       top-level article.  non-null articles are comments
--		       on articles.
--   author_id:	       User_id of article author.
--   creation_date:    Timestamp of when article was created.
--   title:	       Title of article, up to 100 characters.  null for comments.
--   slug:	       URL name of article, e.g., "my-article".  null for comments.
--   body:	       The body text of the article.
--   display:	       Non-zero indicates article should be displayed; zero hides it.
--
create table articles (
       article_id	   serial primary key,
       refers_to	   int8,
       author_id	   int8 not null,
       creation_date	   timestamp (0),
       title		   varchar(100),
       slug		   varchar(100),
       body		   text,
       display		   int4 not null
);


-- discussions
-- Holds data for each discussion post:
--   discussion_id:  Serial, auto-generated key value
--   category:	     One of discussion_categories (see table definition below)
--   refers_to:	     Parent discussion_id.  can be null, which indicates
--   		     top-level forum post.  non-null posts are comments
--		     in discussions.
--   author_id:	     User_id of post author.
--   creation_date:  Timestamp of when post was created.
--   subject:	     Subject of post, up to 100 characters.  null for replies.
--   body:	     The body text of the discussion post.
--   display:	     Non-zero indicates post should be displayed; zero hides it.
--
create table discussions (
       discussion_id	serial primary key,
       category		int4,
       refers_to	int8,
       author_id	int8 not null,
       creation_date	timestamp (0),
       subject		text,
       body		text,
       display		int4 not null
);


-- discussion_categories
-- Categories for discussion posts.  Category 0 shall be the "Miscellaneous" category,
-- which can be used to have one single category as the forum begins, and then split
-- off into multiple categories as needed.
-- category_id:	     Serial, auto-generated key value.
-- category_name:    Name of category (displayed on site).
-- description:	     Description of category (may be displayed on site; currently optional
-- 		     for possible future use).
create table discussion_categories (
	category_id	serial primary key,
	category_name	varchar (100) not null,
	description	text
);


-- events
-- Table for upcoming events.
--   event_id:	      Serial, auto-generated key value.
--   author_id:	      Refers to entry in user table.
--   creation_date:   Timestamp for when the event was created.
--   title:	      Title of event.
--   description:     Description of event.
--   start_date:      Start date of event.
--   end_date:	      End date of event.  If null, event is one day (start_date).
--   display:	      Display level.  0=off, 1=normal, 2...= special categories.
create table events (
      	event_id		serial primary key,
       	-- currently unused, but might be useful someday
       	category		int4,
       	author_id	        int8 not null,
       	creation_date		timestamp (0),
       	title			varchar (300),
       	description		text,
       	start_date		timestamp not null,
	end_date		timestamp,
       	display			int4 not null
);