-- Create data_contracts table
create table data_contracts (
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