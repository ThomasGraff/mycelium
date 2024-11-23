-- Enable necessary extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- Create data_contracts table
create table if not exists data_contracts (
    id text primary key,
    data_contract_specification text not null,
    info jsonb not null,
    servers jsonb,
    terms jsonb,
    models jsonb,
    definitions jsonb,
    examples jsonb,
    service_level jsonb,
    quality jsonb,
    links jsonb,
    tags text[],
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    user_id uuid references auth.users(id)
);

-- Enable RLS
alter table data_contracts enable row level security;

-- Create policies
create policy "Users can view their own data contracts"
    on data_contracts for select
    using (auth.uid() = user_id);

create policy "Users can create their own data contracts"
    on data_contracts for insert
    with check (auth.uid() = user_id);

create policy "Users can update their own data contracts"
    on data_contracts for update
    using (auth.uid() = user_id);

create policy "Users can delete their own data contracts"
    on data_contracts for delete
    using (auth.uid() = user_id);

-- Create trigger for updated_at
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger update_data_contracts_updated_at
    before update on data_contracts
    for each row
    execute function update_updated_at_column(); 